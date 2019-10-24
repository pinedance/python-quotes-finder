def n_gram( text, n ):
    return [ text[i:i+n] for i in range( len( text )-n+1 ) ]

def uniq_gram_between( text1, text2, n ):
    t1_gram = set( n_gram( text1, n ) )
    t2_gram = set( n_gram( text2, n ) )
    t1_uniq_gram = t1_gram.difference( t2_gram )
    t2_uniq_gram = t2_gram.difference( t1_gram )
    return list(t1_uniq_gram), list(t2_uniq_gram)

def uniq_partition( text, uniq_gram, min_partition_size=5 ):
    n_len = len( text )
    n_ = len( uniq_gram[0] )
    uniq_partition = []
    partition_on = True
    partition_size = 0
    start_i = 0
    for i in range(n_len - n_ + 1):
        if text[i:i+n_] in uniq_gram:
            if not partition_on:
                partition_on = True
                partition_size = 0
                start_i = i
            partition_size += 1
        else:
            if partition_on:
                if partition_size >= min_partition_size:
                    uniq_partition.append( (start_i, i) )
                partition_on = False
                partition_size = 0

    return uniq_partition


def merge_partition( partitions, min_ignore_size=5 ):
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


def invert_partiton( partitions, last_i ):
    init = 0
    inverted_partitons = []
    for b, e in partitions:
        if b == 0 : continue
        inverted_partitons.append( (init, b) )
        init = e
    inverted_partitons.append( (init, last_i) )

    return inverted_partitons


def filter_partition_between( text1, text2, n, min_partition_size=5, min_ignore_size=5 ):
    # uniq_gram
    t1_ug, t2_ug = uniq_gram_between( text1, text2, n )
    # uniq_partition
    t1_up = uniq_partition( text1, t1_ug, min_partition_size=min_partition_size )
    t2_up = uniq_partition( text2, t2_ug, min_partition_size=min_partition_size )
    # merged_partition
    t1_mg = merge_partition( t1_up, min_ignore_size=min_ignore_size )
    t2_mg = merge_partition( t2_up, min_ignore_size=min_ignore_size )

    # inverted_partition
    t1_iv = invert_partiton( t1_mg, last_i=len(text1) )
    t2_iv = invert_partiton( t2_mg, last_i=len(text2) )
    return t1_iv, t2_iv
