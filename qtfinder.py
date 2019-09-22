import sys, shutil
from os import path, makedirs
from time import time

from quotes_finder import helper, finder, report
# from quotes_finder.finder import find_substrings
# from quotes_finder.report import save_trg2html, save_result, save_html

def get_params():

    if len( sys.argv ) == 3 :
        ref_path, trg_path = sys.argv[1], sys.argv[2]
        output_path = helper.get_output_path()
    elif len( sys.argv ) == 4:
        ref_path, trg_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print( "USE LIKE THIS: \npython findqt.py [REF_FILE_PATH] [TARGET_FILE_PATH] {[OUTPUT_PATH]}" )
        exit()

    if not path.isfile( ref_path ):
        print( "There is no {}".format(ref_path) )
        exit()

    if not path.isfile( trg_path ):
        print( "There is no {}".format(trg_path) )
        exit()

    if path.exists( output_path ):
        print("Output path {} is already there.".format( output_path) )
        exit()
        # shutil.rmtree( output_path )

    print("# REF : {}".format( ref_path ) )
    print("# TRG : {}".format( trg_path ) )
    print("# OUTPUT : {}".format( output_path ) )

    return ref_path, trg_path, output_path

def main( ref_path, trg_path, output_path ):

    with open(ref_path, 'r', encoding="utf-8") as fl:
        ref_raw = fl.read()

    with open(trg_path, 'r', encoding="utf-8") as fl:
        trg_raw = fl.read()

    q_ = time()
    print( "\n" + ("=" * 80) )
    print( ">> Let's Begin ... ")
    print( "   It takes a long time. You better to take a nap." )
    print( "=" * 80)

    print("# Making Output Directory ... ")
    makedirs( output_path )

    indices, indices_with_overlap = finder.find_substrings( ref_raw, trg_raw, min_len=12 )
    report.save_result2html( ref_raw, trg_raw, indices_with_overlap, output_path )

    print( "End ...  {:0.3f}\n\n".format( time()-q_ ) )


main( *get_params() )
