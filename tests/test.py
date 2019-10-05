import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from quotesfinder import helper, finder, report

ref_raw = "天癸至, 精氣溢寫, 陰陽和, 故能有子; 三八, 腎氣平均, 筋骨勁强, 故眞牙生而長極; 四八, 筋骨隆盛, 肌肉滿壯"
trg_raw = "大衝脈盛。月事以時下。故有子。三七。腎氣平均。故眞牙生而長極。四七。筋骨堅。"
indices, indices_with_overlap = finder.find_substrings( ref_raw, trg_raw, min_len=12, verbose=True )
report.save_result2html( ref_raw, trg_raw, indices_with_overlap, "output.html" )
