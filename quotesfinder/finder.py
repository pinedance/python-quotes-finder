#!/usr/bin/env python
# coding: utf-8

# # Code

from .hanzi import strip_nonhanzi, restore_index
from .tool import remove_overlap
from .SmithWaterman import smith_waterman
from .SmithWatermanSkip import smith_waterman as smith_waterman_skip

def get_new_idx( raw_idx, ref_idx, trg_idx ):
    new_idx = []
    for ( i_b, i_e ), ( j_b, j_e)  in raw_idx:
        new_idx.append( ( ( ref_idx.index( i_b ), ref_idx.index( i_e ) ), ( trg_idx.index(j_b), trg_idx.index(j_e) ) ) )
    return new_idx

def find_substrings( ref, trg, match_score=3, gap_cost=2, min_len=8, verbose=True, debug=False, skip=False, \
                     n=3, max_gap=3 ):

    if verbose: print("# Texts Preprocessing")
    ref_han, ref_non_han = strip_nonhanzi( ref )
    trg_han, trg_non_han = strip_nonhanzi( trg )

    ref_idx = restore_index(ref_han, ref_non_han )
    trg_idx = restore_index(trg_han, trg_non_han )

    if verbose: print("# Finding Similar Substrings")
    if skip:
        raw_idx_with_overlap = smith_waterman_skip( ref_han, trg_han, match_score=match_score, gap_cost=gap_cost, min_len=min_len, debug=debug, verbose=verbose, \
                                                    n=n, max_gap=max_gap )
    else:
        raw_idx_with_overlap = smith_waterman( ref_han, trg_han, match_score=match_score, gap_cost=gap_cost, min_len=min_len, debug=debug, verbose=verbose )
    raw_idx = remove_overlap( trg_han, raw_idx_with_overlap, verbose=verbose )

    if verbose: print("# Building new indices")
    new_idx_with_overlap = get_new_idx( raw_idx_with_overlap, ref_idx, trg_idx )
    new_idx = get_new_idx( raw_idx, ref_idx, trg_idx )

    return new_idx, new_idx_with_overlap
