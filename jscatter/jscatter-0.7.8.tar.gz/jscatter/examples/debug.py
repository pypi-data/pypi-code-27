# -*- coding: utf-8 -*-
#  this file is intended to used in the debugger
# write a script that calls your function to debug it

import jscatter as js
import numpy as np
import sys
# some arrays
w=np.r_[-100:100]
q=np.r_[0:10:0.1]
x=np.r_[1:10]


import jscatter as js
import numpy as np
import glob
from scipy import ndimage
from numpy import ma


sc=js.sf.scLattice(0.3,40)
sc.set_b(0)
sc.inEllipsoid([0,0,0],[1,0,0],4,5)
sc.show()



