from __future__ import absolute_import
from __future__ import print_function
import os
import sys
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer

codedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/verilogcode/'

expected = """\
(Bind dest:TOP.cnt \
tree:(Branch Cond:(Partselect Var:(Terminal TOP.RST) MSB:(IntConst 0) LSB:(IntConst 0)) \
True:(IntConst 'd0)))
"""

def test():
    filelist = [codedir + 'ptr_clock_reset.v']
    topmodule = 'TOP'
    noreorder = False
    nobind = False
    include = None
    define = None
    
    analyzer = VerilogDataflowAnalyzer(filelist, topmodule,
                                       noreorder=noreorder,
                                       nobind=nobind,
                                       preprocess_include=include,
                                       preprocess_define=define)
    analyzer.generate()

    directives = analyzer.get_directives()
    instances = analyzer.getInstances()
    terms = analyzer.getTerms()
    binddict = analyzer.getBinddict()

    output = []
    output.append(list(binddict.values())[0][0].tostr())
    output.append('\n')
            
    rslt = ''.join(output)

    print(rslt)
    assert(rslt == expected)
    
    assert(list(binddict.values())[0][0].getClockBit() == 2)
    assert(list(binddict.values())[0][0].getResetBit() == 0)

if __name__ == '__main__':
    test()
