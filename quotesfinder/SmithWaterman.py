#!/usr/bin/env python
# coding: utf-8

from tqdm import tqdm as tqdm
from time import time
from .report import save_result

# ### Operate SmithWaterman Algorithm

def build_matrix(a, b, match_score=3, gap_cost=2, debug=False, verbose=True ):

    len_a = len(a)
    len_b = len(b)
    if verbose: print( "* Complexity: {:,} ({:,} × {:,})".format( len_a * len_b, len_a, len_b ) )
    H, P = {}, {}

    for i in tqdm( range( 1, len_a+1 ), disable=(not verbose) ):
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
        print(H)
        print(P)

    return H, P


def traceback( P, xy, trace_history={} ):
    end_i, end_j = xy
    # 경로겹침시 (-1, -1) 반환
    if trace_history.get(xy): return (-1, -1), trace_history
    trace_history[xy] = 1

    value = P.get( (end_i, end_j), 0 )
    if value == 1 : new_i, new_j = end_i - 1, end_j - 1
    elif value == 2 : new_i, new_j = end_i - 1, end_j
    elif value == 3 : new_i, new_j = end_i, end_j - 1
    else:
        return (end_i, end_j), trace_history
    return traceback( P, (new_i, new_j), trace_history )


def smith_waterman(a, b, match_score=3, gap_cost=2, min_len=8, debug=False, verbose=True ):
    """
    a : source
    b : target
    """
    cutoff = min_len * match_score

    if verbose: print( "* Build Matrix ... ")
    _q = time()

    # different from skip version
    H, P = build_matrix(a, b, match_score=match_score, gap_cost=gap_cost, debug=debug, verbose=verbose )
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
