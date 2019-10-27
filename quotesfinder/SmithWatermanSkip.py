#!/usr/bin/env python
# coding: utf-8

from time import time
from itertools import chain

from tqdm import tqdm as tqdm

from .text import get_attention_each
from .report import save_result
from .SmithWaterman import traceback

# ### Operate SmithWaterman Algorithm

def build_matrix( a, b, match_score=3, gap_cost=2, debug=False, verbose=True, \
                  n=3, min_len=8, max_gap=3 ):

    len_a = len(a)
    len_b = len(b)
    if verbose: print( "* Complexity: {:,} ({:,} × {:,})".format( len_a * len_b, len_a, len_b ) )
    H, P = {}, {}

    a_attention, b_attention = get_attention_each(a, b, n=n, min_len=min_len, max_gap=max_gap, verbose=verbose )
    if debug:
        print("a_attention", a_attention)
        print("b_attention", b_attention)

    a_ranges = list( chain( *[ range(p+1, q+1) for p, q in a_attention ] ) )
    b_ranges = list( chain( *[ range(p+1, q+1) for p, q in b_attention ] ) )
    len_a_attention = sum( [ q-p+1 for p, q in a_attention ] )
    len_b_attention = sum( [ q-p+1 for p, q in b_attention ] )
    if verbose: print( "* Complexity(Skiped): {:,} ({:,} × {:,})".format( len_a_attention * len_b_attention, len_a_attention, len_b_attention ) )

    for i in tqdm( a_ranges, disable=(not verbose) ):
        for j in b_ranges:
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
        print("*", i, j)
        print(H)
        print(P)

    return H, P

def smith_waterman( a, b, match_score=3, gap_cost=2, min_len=8, debug=False, verbose=True,\
                    n=3, max_gap=3 ):
    """
    a : source
    b : target
    """
    cutoff = min_len * match_score

    if verbose: print( "* Build Matrix ... ")
    _q = time()

    # different from original version
    H, P = build_matrix( a, b, match_score=match_score, gap_cost=gap_cost, debug=debug, verbose=verbose,\
                         n=n, min_len=min_len, max_gap=max_gap )
    ###

    H_lst = H.items()
    H_sorted = sorted( H_lst, key=lambda x: ( x[1], x[0][1] ), reverse=True )
    if verbose: print( "  ... {:0.3f}".format( time()-_q ) )
    if debug: print( H_sorted )

    # get all sets
    if verbose: print( "* Traceback ... ")
    _q = time()
    quotes_all = []
    # traceback history를 기억해 두었다가 경로가 중첩되는 경우는 버림
    trace_history = {}
    for (i, j), value in tqdm( H_sorted, disable=(not verbose) ):
        if value < cutoff : continue
        # 시작점의 경로중첩 확인
        if trace_history.get( (i,j) ) : continue
        if debug: print( i, j )
        end_i, end_j = i, j
        (begin_i, begin_j), trace_history = traceback( P, (end_i, end_j), trace_history )
        # 경로 추정 중 경로중첩이 일어나면 버림
        if (begin_i, begin_j) == (-1,-1) : continue
        quotes_all.append( ( (begin_i, end_i), (begin_j, end_j) ) )     # string[begin:end]
    if verbose: print( "  ... {:0.3f}".format( time()-_q ) )
    # save_result( trace_history, "trace_history")
    if debug:
        print( "trace_history:", trace_history )

    if verbose: print( "* Complete! ")
    return sorted( quotes_all, key=lambda x: (x[1][0], -x[1][1]) )
