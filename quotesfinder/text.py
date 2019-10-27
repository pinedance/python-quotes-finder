from tqdm import tqdm
from time import time
import re

def n_gram( text, n ):
    return [ text[i:i+n] for i in range( len( text )-n+1 ) ]

def uniq_gram_between( text1, text2, n ):
    t1_gram = set( n_gram( text1, n ) )
    t2_gram = set( n_gram( text2, n ) )
    t1_uniq_gram = t1_gram.difference( t2_gram )
    t2_uniq_gram = t2_gram.difference( t1_gram )
    return list(t1_uniq_gram), list(t2_uniq_gram)

def uniq_partition( text, uniq_gram, min_partition_size=8, min_ignore_size=1, verbose=True ):
    n_len = len( text )
    n_ = len( uniq_gram[0] )
    alpha = int( n_ / 2 )

    if verbose: print( "└ Getting Uniq Indexs")
    _uniq_idxs = sum( [ [ m.start() for m in re.finditer(uq, text) ] for uq in uniq_gram ], []  )
    uniq_idxs = sorted( _uniq_idxs )

    uniq_partition = []
    start_i = uniq_idxs[0]

    if verbose: print( "└ Getting Uniq Ranges of {}……{}".format(text[0:8], text[-8:]))
    for k in tqdm( range( len(uniq_idxs) ), disable=(not verbose) ):
        if k == 0 : continue
        if (uniq_idxs[k] - uniq_idxs[k-1] - 1 ) < min_ignore_size: continue
        if (uniq_idxs[k-1] - start_i) < min_partition_size: continue
        uniq_partition.append( ( start_i, uniq_idxs[k-1] ) )
        start_i = uniq_idxs[k]
    if (uniq_idxs[-1] - start_i) >= min_partition_size:
        uniq_partition.append( ( start_i, uniq_idxs[-1] ) )

    return uniq_partition

"""
def merge_partition( partitions, min_ignore_size=1 ):
    start_i = partitions[0][0]
    last_end_i = partitions[0][1]
    merged_partitions = []
    for b, e in partitions[1:]:
        if (b-last_end_i) > min_ignore_size:
            merged_partitions.append( (start_i, last_end_i) )
            start_i = b
        last_end_i = e
    merged_partitions.append( (start_i, last_end_i) )
    return merged_partitions
"""

def invert_partiton( partitions, last_i, min_len=8 ):
    init = 0
    inverted_partitons = []
    for b, e in partitions:
        if b == 0 : continue
        if (b - init) >= min_len:
            inverted_partitons.append( (init, b) )
        init = e
    if (last_i - init) >= min_len:
        inverted_partitons.append( (init, last_i) )

    return inverted_partitons


def filter_partition_between( text1, text2, n=3, min_partition_size=8, min_ignore_size=1, verbose=True ):
    # uniq_gram
    if verbose: print( "# Calculate Skip partitions " )
    if verbose: print( "* Getting n_grams ..." )
    t1_ug, t2_ug = uniq_gram_between( text1, text2, n )
    # uniq_partition
    if verbose: print( "* Getting Uniq partitions ..." )
    _q = time()
    t1_up = uniq_partition( text1, t1_ug, min_partition_size=min_partition_size, min_ignore_size=min_ignore_size, verbose=verbose )
    t2_up = uniq_partition( text2, t2_ug, min_partition_size=min_partition_size, min_ignore_size=min_ignore_size, verbose=verbose )
    if verbose: print( "  ... {:0.3f}".format( time()-_q ) )

    """
    # merged_partition
    if verbose: print( "* Merging small partitons ..." )
    t1_mg = merge_partition( t1_up, min_ignore_size=min_ignore_size )
    t2_mg = merge_partition( t2_up, min_ignore_size=min_ignore_size )
    """

    # inverted_partition
    if verbose: print( "* Inverting Uniq partitions ..." )
    t1_iv = invert_partiton( t1_up, last_i=len(text1), min_len=min_partition_size )
    t2_iv = invert_partiton( t2_up, last_i=len(text2), min_len=min_partition_size )
    return t1_iv, t2_iv
