import sys, shutil
from os import path, makedirs
from time import time

from quotesfinder import helper, finder, report

def get_params():

    output_path_serial = helper.get_timestamp()

    if len( sys.argv ) == 3 :
        ref_path, trg_path = sys.argv[1], sys.argv[2]
        output_path = 'output-' + output_path_serial
    elif len( sys.argv ) == 4:
        ref_path, trg_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print( "USE LIKE THIS: \npython findqt.py [REF_FILE_PATH] [TARGET_FILE_PATH] {[OUTPUT_PATH]}" )
        sys.exit()

    if not path.isfile( ref_path ):
        print( "There is no {}".format(ref_path) )
        sys.exit()

    if not path.isfile( trg_path ):
        print( "There is no {}".format(trg_path) )
        sys.exit()

    if path.exists( output_path ):
        print("Output path {} is already there.".format( output_path) )
        # sys.exit()
        # shutil.rmtree( output_path )
        output_prefix = output_path_serial
    else:
        print("# Making Output Directory ... ")
        makedirs( output_path )
        output_prefix = ""

    print("# REF : {}".format( ref_path ) )
    print("# TRG : {}".format( trg_path ) )
    print("# OUTPUT : {}".format( output_path ) )

    return ref_path, trg_path, output_path, output_prefix

def main():

    ref_path, trg_path, output_path, output_prefix = get_params()

    with open(ref_path, 'r', encoding="utf-8") as fl:
        ref_raw = fl.read()

    with open(trg_path, 'r', encoding="utf-8") as fl:
        trg_raw = fl.read()

    ref_raw = ref_raw.strip()
    trg_raw = trg_raw.strip()

    q_ = time()
    print( "\n" + ("=" * 80) )
    print( ">> Let's Begin ... ")
    print( "   It takes a long time. You better to take a nap." )
    print( "=" * 80)

    indices, indices_with_overlap = finder.find_substrings( ref_raw, trg_raw, min_len=12 )
    report.save_result2html( ref_raw, trg_raw, indices_with_overlap, "{}/{}result.html".format( output_path, output_prefix ) )
    report.save_html( ref_raw, trg_raw, indices_with_overlap, "{}/{}result_pair.html".format( output_path, output_prefix )  )
    print( "End ...  {:0.3f}\n\n".format( time()-q_ ) )


if __name__ == "__main__":
    main()
