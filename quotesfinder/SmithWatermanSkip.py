#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm as tqdm
from time import time
from .text import filter_partition_between
from .report import save_result
from .SmithWaterman import traceback

# ### Operate SmithWaterman Algorithm

def build_matrix(a, b, match_score=3, gap_cost=2, debug=False, verbose=True, \
                 min_len=8, min_ignore_size=1 ):

    len_a = len(a)
    len_b = len(b)
    if verbose: print( "* Complexity: {:,} ({:,} × {:,})".format( len_a * len_b, len_a, len_b ) )
    H, P = {}, {}

    a_range, b_range = filter_partition_between(a, b, min_partition_size=min_len, min_ignore_size=min_ignore_size, verbose=verbose )
    a_skiped = sum( [ list( range(a+1, b+1) ) for a, b in a_range ], [] )
    b_skiped = sum( [ list( range(a+1, b+1) ) for a, b in b_range ], [] )
    len_a_skiped = len(a_skiped)
    len_b_skiped = len(b_skiped)
    if verbose: print( "* Complexity(Skiped): {:,} ({:,} × {:,})".format( len_a_skiped * len_b_skiped, len_a_skiped, len_b_skiped ) )

    for i in tqdm( a_skiped, disable=(not verbose) ):
        for j in b_skiped:
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
        print(H)
        print(P)

    return H, P

def smith_waterman(a, b, match_score=3, gap_cost=2, min_len=8, debug=False, verbose=True,\
                    min_ignore_size=1 ):
    """
    a : source
    b : target
    """
    cutoff = min_len * match_score

    if verbose: print( "* Build Matrix ... ")
    _q = time()

    # different from original version
    H, P = build_matrix(a, b, match_score, gap_cost, debug=debug, verbose=verbose,\
                        min_len=min_len, min_ignore_size=min_ignore_size)
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
