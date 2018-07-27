import sys

if sys.version[0] == '2':
    from .funclib_conf import *
    from .funclib import FuncLib as fn
else:
    from funclib.funclib_conf import *
    from funclib.funclib import FuncLib as fn
