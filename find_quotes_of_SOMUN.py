from time import time
from lib.quotes_finder import find_substrings, print_trg2html


txt1_path = "DATA/SOMUN.TN.txt"
txt2_path = "DATA/DYBG.TN.txt"

with open(txt1_path, 'r', encoding="utf-8") as fl:
    txt1_raw = fl.readlines()

with open(txt2_path, 'r', encoding="utf-8") as fl:
    txt2_raw = fl.read()


def main():
    
    ref_raw = txt2_raw
    
    for chapter_n in range(1, 81):
        q_ = time()
        print( "Begin ... chapter {:02d}".format(chapter_n) )
        trg_raw = txt1_raw[ chapter_n ]  # 소문 편
        new_indices, raw_indices = find_substrings( ref_raw, trg_raw, min_len=8 )
        print_trg2html( trg_raw, new_indices, "OUTPUT/SOMUN{:02d}.html".format(chapter_n), eol="{n}" )
        print( "End ... chapter {:02d} / {:0.3f}".format( chapter_n, time()-q_ ) )


main()