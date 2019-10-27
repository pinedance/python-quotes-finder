from tqdm import tqdm
from time import time
import re
from itertools import chain

def n_gram( text, n ):

    return [ text[i:i+n] for i in range( len( text )-n+1 ) ]

def get_common_gram_between( text1, text2, n ):

    t1_gram = set( n_gram( text1, n ) )
    t2_gram = set( n_gram( text2, n ) )
    common_gram = t1_gram & t2_gram

    return list(common_gram)

def get_attention( text, common_gram, min_len=8, max_gap=3, verbose=True ):

    if verbose: print( "└ Getting Attention Index")
    _att_idxs =  [ [ list(range(m.start(), m.end())) for m in re.finditer(cg, text) ] for cg in common_gram ]
    _att_idxs = chain.from_iterable( chain.from_iterable( _att_idxs ) )
    att_idxs = sorted( list( set( _att_idxs) ) )

    attention = []
    start_i = att_idxs[0]

    if verbose: print( "└ Getting Attention Parts of {}……{}".format(text[0:8], text[-8:]))
    for k in tqdm( range( len( att_idxs ) ), disable=(not verbose) ):
        if k == 0 : continue
        if (att_idxs[k] - att_idxs[k-1] ) < max_gap: continue
        if (att_idxs[k-1] - start_i) < min_len: continue
        attention.append( ( start_i, att_idxs[k-1] ) )
        start_i = att_idxs[k]
    if (att_idxs[-1] - start_i) >= min_len:
        attention.append( ( start_i, len(text) ) )

    return attention


def get_attention_each( text1, text2, n=3, min_len=8, max_gap=3, verbose=True ):

    # uniq_gram
    if verbose: print( "# Calculate Attention Parts" )
    if verbose: print( "* Getting n_grams ..." )
    common_gram = get_common_gram_between( text1, text2, n )

    # uniq_partition
    if verbose: print( "* Getting Attention Parts ..." )
    _q = time()
    t1_attention = get_attention( text1, common_gram, min_len=min_len, max_gap=max_gap, verbose=verbose )
    t2_attention = get_attention( text2, common_gram, min_len=min_len, max_gap=max_gap, verbose=verbose )
    if verbose: print( "  ... {:0.3f}".format( time()-_q ) )

    return t1_attention, t2_attention
