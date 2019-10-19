from tqdm import tqdm as tqdm
from time import time

def remove_overlap(trg, indices, verbose=False ):
    # remove overlap ranges
    if verbose: print( "* Remove Overlap ... ")
    _q = time()

    occupation = [0] * (len( trg ) + 1)
    quotes = []
    for elem in tqdm( indices, disable=(not verbose) ):
        (_, _), (b_j, e_j) = elem
        if sum( occupation[b_j:e_j] ) > 0: continue
        quotes.append( elem )
        occupation[b_j:e_j] = [1] * ( e_j - b_j )
    if verbose: print( "  ... {:0.3f}".format( time()-_q ) )
    return sorted( quotes, key=lambda x: x[1][0] )
