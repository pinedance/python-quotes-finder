#!/usr/bin/env python
# coding: utf-8


import regex as re
from blist import blist

def strip_nonhanzi( text ):

    # hanzi 범위
    cjk_range_pattern = re.compile( "[\p{Han}]", re.UNICODE )
    non_cjk_range_pattern = re.compile( "[^\p{Han}]", re.UNICODE )

    # hanzi 추출
    only_hanzi = "".join( re.findall( cjk_range_pattern, text  ) )
    non_hanzi = [ ( m.start(0), m.group(0) ) for m in re.finditer( non_cjk_range_pattern, text ) ]

    return only_hanzi, non_hanzi



def restore_index( text_han, non_han ):

    idx_list = blist( range( len( text_han ) +1 ) )

    for j, char in sorted(non_han, key=lambda x: x[0]):
        idx_list.insert(j, char)

    return idx_list
