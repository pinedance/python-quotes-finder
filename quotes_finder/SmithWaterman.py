#!/usr/bin/env python
# coding: utf-8

import numpy as np
from tqdm import tqdm as tqdm
from time import time

# ### Operate SmithWaterman Algorithm

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


def traceback( P, xy ):
    end_i, end_j = xy

    value = P.get( (end_i, end_j), 0 )
    if value == 1 : new_i, new_j = end_i - 1, end_j - 1
    elif value == 2 : new_i, new_j = end_i - 1, end_j
    elif value == 3 : new_i, new_j = end_i, end_j - 1
    else:
        return end_i, end_j
    return traceback( P, (new_i, new_j) )


def smith_waterman(a, b, match_score=3, gap_cost=2, min_len=8, overlap=False, debug=False ):
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
    if overlap:
        quotes = quotes_all
    else:
        occupation = [0] * (len(b) + 1)
        quotes = []
        for elem in tqdm(quotes_all):
            (_, _), (b_j, e_j) = elem
            if sum( occupation[b_j:e_j] ) > 0: continue
            quotes.append( elem )
            occupation[b_j:e_j] = [1] * ( e_j - b_j )
    print( "  ... {:0.3f}\n".format( time()-_q ) )

    print( "* Complete!\n ")
    return sorted( quotes, key=lambda x: (x[1][0], -x[1][1]) )
