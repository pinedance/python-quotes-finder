#!/usr/bin/env python
# coding: utf-8

# From finder.SmithWaterman.v2

# # 인용 구문 찾기 ( feat. Smith-Waterman )

# 한의학 서적에는 많은 구문들이 상호 인용 관계를 맺고 있다. 이런 인용구문들은 명시적인 경우도 있지만 그렇지 않은 경우도 있다. 후자의 경우 이를 알아차리는 것은 매우 어렵다. 전자의 경우라 하더라도 어디까지 인용되었는지 모호한 경우가 많기 때문에 원문을 찾고 확인해야 하는 경우가 많다.
#
# 2가지 텍스트가 주어졌을 때, 상호 인용관계를 맺는 구문을 자동으로 찾는 방법을 모색해 보았다.
#
# 텍스트는 편의상 참조된 텍스트(REF), 참조한 텍스트(TRG)으로 구분할 수 있다. REF는 시대적으로 더 앞선 문헌으로 TRG가 이를 참고하여 구문을 인용할 수 있어야 한다.
#
# TRG는 REF의 여러 부분을 인용할 수 있다. 따라서 최종 인용구문 결과에서 TRG의 구절은 중복되는 부분이 있어서는 안되지만, REF의 구절은 중복이 발생할 수도 있다. 중복된 부분은 2번 이상 인용된 부분이다.
#
# 중복된 부분을 찾는 방법으로 Smith-Waterman 알고리즘을 사용하였다. 글자의 일치, 추가, 삭제에 대한 점수를 부여하여 글자 단위로 상호 비교를 통해 유사한 문자열을 찾는 방법이다. 원하는 결과를 도출할 수 있는 좋은 방법이지만, 글자와 글자를 하나 하나 대조하기 때문에 연산에 많은 시간이 소요된다.

# # Code

# ## Lib

# In[36]:


import numpy as np
import regex as re
from tqdm import tqdm as tqdm
from time import time
import random


# ### Operate SmithWaterman Algorithm

# In[2]:


def build_matrix(a, b, match_score=3, gap_cost=2, debug=False):

    len_a = len(a)
    len_b = len(b)
    print( "* Complexity: {:,} ({:,} × {:,})".format( len_a * len_b, len_a, len_b ) )
    H, P = {}, {}

    if debug:
        H_ = np.zeros( ( len_a + 1, len_b + 1), np.int)
        P_ = np.zeros( ( len_a + 1, len_b + 1), np.int)

    for i in tqdm( range( 1, len_a+1 ) ):
        for j in range( 1, len_b+1 ):
            match = H.get( (i - 1, j - 1 ), 0 ) + ( match_score if a[i - 1] == b[j - 1] else - match_score )
            delete = H.get( (i - 1, j ), 0 )  - gap_cost
            insert = H.get( (i , j - 1 ), 0 )  - gap_cost
            values = [ 0, match, delete, insert ]
            mx = max( values )
            if mx == 0 : continue
            argmax = values.index( mx )
            H[ (i, j) ] = mx
            P[ (i, j) ] = argmax

            if debug:
                H_[i,j] = mx
                P_[i,j] = argmax

    if debug:
        print(H_)
        print(P_)

    return H, P


# In[3]:


def traceback( P, xy ):
    end_i, end_j = xy

    value = P.get( (end_i, end_j), 0 )
    if value == 1 : new_i, new_j = end_i - 1, end_j - 1
    elif value == 2 : new_i, new_j = end_i - 1, end_j
    elif value == 3 : new_i, new_j = end_i, end_j - 1
    else:
        return end_i, end_j
    return traceback( P, (new_i, new_j) )


# In[4]:


def smith_waterman(a, b, match_score=3, gap_cost=2, min_len=8, debug=False ):
    """
    a : source
    b : target
    """
    cutoff = min_len * match_score
    print( "* Build Matrix ... ")
    _q = time()
    H, P = build_matrix(a, b, match_score, gap_cost, debug=debug )
    H_lst = H.items()
    H_sorted = sorted( H_lst, key=lambda x: ( x[1], x[0][1] ), reverse=True )
    print( "  ... {:0.3f}\n".format( time()-_q ) )

    # get all sets
    print( "* Traceback ... ")
    _q = time()
    quotes_all = []
    for (i, j), value in tqdm(H_sorted):
        if value < cutoff : continue
        end_i, end_j = i, j
        begin_i, begin_j = traceback( P, (end_i, end_j) )
        quotes_all.append( ( (begin_i, end_i), (begin_j, end_j) ) )     # string[begin:end]
    print( "  ... {:0.3f}\n".format( time()-_q ) )

    # remove overlap ranges
    print( "* Refine outputs ... ")
    _q = time()
    occupation = [0] * (len(b) + 1)
    quotes = []
    for elem in tqdm(quotes_all):
        (_, _), (b_j, e_j) = elem
        if sum( occupation[b_j:e_j] ) > 0: continue
        quotes.append( elem )
        occupation[b_j:e_j] = [1] * ( e_j - b_j )
    print( "  ... {:0.3f}\n".format( time()-_q ) )
    print( "* Complete!\n ")
    return sorted( quotes, key=lambda x: x[1][0] )


# ### Operate Texts

# In[5]:


def strip_nonhanzi( text ):

    # hanzi 범위
    cjk_range_pattern = re.compile( "[\p{Han}]", re.UNICODE )
    non_cjk_range_pattern = re.compile( "[^\p{Han}]", re.UNICODE )

    # hanzi 추출
    only_hanzi = "".join( re.findall( cjk_range_pattern, text  ) )
    non_hanzi = [ ( m.start(0), m.group(0) ) for m in re.finditer( non_cjk_range_pattern, text ) ]

    return only_hanzi, non_hanzi


# In[6]:


def restore_index( text_han, non_han ):

    idx_list = list( range( len( text_han ) +1 ) )

    for j, char in sorted(non_han, key=lambda x: x[0]):
        idx_list.insert(j, char)

    return idx_list


# ### Operate Outputs

# In[7]:


def print_output(a, b, indices ):

    for (i1,i2), (j1,j2) in indices:
        print( "TRG：{:08d}-{:08d}\t{}".format( j1, j2, b[j1:j2] ) )
        print( "SRC：{:08d}-{:08d}\t{}".format( i1, i2, a[i1:i2] ) )
        print()


# In[8]:


def print_html(a, b, indices ):

    style = """
    <style>
    .match {
        color: blue;
    }
    </style>
    """

    filename = ""
    handler = open("finder.SmithWaterman.v2.html", 'w', encoding="utf-8")
    i = 1
    border_size = 20
    for ( i_b, i_e ), ( j_b, j_e)  in indices:
        handler.write( "<div>" )
        handler.write( "\t<h2>{:d}</h2>\n".format(i) )
        handler.write( "\t<p class='rtg'>TRG：{}<span class='match'>{}</span>{}</p>".format( b[j_b-border_size:j_b], b[j_b:j_e], b[j_e:j_e+border_size] ) )
        handler.write( "\t<p class='ref'>SRC：{}<span class='match'>{}</span>{}</p>".format( a[i_b-border_size:i_b], a[i_b:i_e], a[i_e:i_e+border_size] ) )
        handler.write( "\n</div>" )
        handler.write( "<br><br>")
        i += 1

    handler.write( style )
    handler.close()


# In[49]:


def print_trg2html(trg, indices, filename, eol, color="random" ):

    style = "    <style>\n    .match {{ \n        color: {};\n    }}\n    </style>\n    ".format( color )
    handler = open( filename, 'w', encoding="utf-8")

    rst = ""
    len_idx = len( indices )

    r = lambda: random.randint(50,255)
    g = lambda: random.randint(50,220)
    b = lambda: random.randint(50,255)

    for k, ( ( i_b, i_e ), ( j_b, j_e) ) in enumerate(indices):

        rgb = '#{:02x}{:02x}{:02x}'.format(r(), g(), b())

        last_idx = indices[k-1][1][1] if k != 0 else 0
        comming_idx = indices[k+1][1][1] if k !=(len_idx-1) else -1

        rst = rst +\
            trg[last_idx:j_b] +\
            "<span class='match' id='ref{:03d}' style='color:{};'>".format(k+1, rgb) +\
            trg[j_b:j_e] +\
            "</span>" +\
            trg[i_e:comming_idx]

        if k != (len_idx-1):
            rst = rst + trg[-1]

    if eol:
        rst = rst.replace( eol, "<br>" )

    handler.write( rst )
#     handler.write( style )
    handler.close()


# ### Operate Projects

# In[10]:


def find_substrings( ref, trg, min_len=8 ):

    print("# Texts Preprocessing")
    ref_han, ref_non_han = strip_nonhanzi( ref )
    trg_han, trg_non_han = strip_nonhanzi( trg )

    ref_idx = restore_index(ref_han, ref_non_han )
    trg_idx = restore_index(trg_han, trg_non_han )

    print("# Finding Similar Substrings")
    raw_idx = smith_waterman( ref_han, trg_han, min_len=min_len )

    print("# Building new indices")
    new_idx = []
    for ( i_b, i_e ), ( j_b, j_e)  in raw_idx:
        new_idx.append( ( ( ref_idx.index( i_b ), ref_idx.index( i_e ) ), ( trg_idx.index(j_b), trg_idx.index(j_e) ) ) )

    return new_idx, raw_idx




# ## REF

# https://tiefenauer.github.io/blog/smith-waterman/
