#!/usr/bin/env python
# coding: utf-8

import sys
import random, json

def print_output(a, b, indices ):

    for (i1,i2), (j1,j2) in indices:
        print( "TRG：{:08d}-{:08d}\t{}".format( j1, j2, b[j1:j2] ) )
        print( "SRC：{:08d}-{:08d}\t{}".format( i1, i2, a[i1:i2] ) )
        print()

def save_result( data, filename ):
    sys.stdout = open(filename, 'w')
    print( data )
    sys.stdout = sys.__stdout__

def save_html(a, b, indices, filename ):

    handler = open(filename, 'w', encoding="utf-8")
    i = 1
    border_size = 20
    for ( i_b, i_e ), ( j_b, j_e)  in indices:
        handler.write( "<div>" )
        handler.write( "\t<h2>{:d}</h2>\n".format(i) )
        handler.write( "\t<p class='rtg'>TRG：{}<span class='match'>{}</span>{}</p>".format( b[j_b-border_size:j_b], b[j_b:j_e], b[j_e:j_e+border_size] ) )
        handler.write( "\t<p class='ref'>SRC：{}<span class='match'>{}</span>{}</p>".format( a[i_b-border_size:i_b], a[i_b:i_e], a[i_e:i_e+border_size] ) )
        handler.write( "\n</div>" )
        handler.write( "<br><br>")
        i += 1

    style = """
    <style>
    .match {
    color: blue;
    }
    </style>
    """

    handler.write( style )
    handler.close()


def save_trg2html(trg, indices, filename, eol, color="random" ):

    style = "    <style>\n    .match {{ \n        color: {};\n    }}\n    </style>\n    ".format( color )
    handler = open( filename, 'w', encoding="utf-8")

    rst = ""
    len_idx = len( indices )

    r = lambda: random.randint(50,255)
    g = lambda: random.randint(50,220)
    b = lambda: random.randint(50,255)

    if len_idx > 1 :
        for k, ( ( i_b, i_e ), ( j_b, j_e) ) in enumerate(indices):

            rgb = '#{:02x}{:02x}{:02x}'.format(r(), g(), b())

            last_idx = indices[k-1][1][1] if k != 0 else 0
            comming_idx = indices[k+1][1][1] if k !=(len_idx-1) else -1

            rst = rst +\
                trg[last_idx:j_b] +\
                "<span class='match' id='ref{:03d}' style='color:{};'>".format(k+1, rgb) +\
                trg[j_b:j_e] +\
                "</span>" +\
                trg[i_e:comming_idx]

            if k != (len_idx-1):
                rst = rst + trg[-1]
    else:
        rst = trg

    if eol:
        rst = rst.replace( eol, "<br>" )

    handler.write( rst )
#     handler.write( style )
    handler.close()

def save_result2html( ref_raw, trg_raw, indices, filename ):

    tmp_path = "./quotes_finder/templates/result"
    html_path = tmp_path + ".html"
    js_path = tmp_path + ".js"
    css_path = tmp_path + ".css"

    with open( html_path, 'r', encoding="utf-8") as fl:
        rst = fl.read()

    with open( js_path, 'r', encoding="utf-8") as fl:
        js = fl.read()

    with open( css_path, 'r', encoding="utf-8") as fl:
        css = fl.read()

    ref_indices = sorted(indices, key=lambda x: (x[0][0], -x[0][1]) )
    trg_indices = sorted(indices, key=lambda x: (x[1][0], -x[1][1]) )

    rst = rst.replace( "{{RESULT_JS}}", js )
    rst = rst.replace( "{{RESULT_CSS}}", css )

    rst = rst.replace( "{{REF_TEXT}}", ref_raw )
    rst = rst.replace( "{{TRG_TEXT}}", trg_raw )
    rst = rst.replace( "{{REF_INDICES}}", json.dumps( ref_indices ) )
    rst = rst.replace( "{{TRG_INDICES}}", json.dumps( trg_indices ) )

    with open( filename, 'w', encoding="utf-8") as fl:
        fl.write( rst )
