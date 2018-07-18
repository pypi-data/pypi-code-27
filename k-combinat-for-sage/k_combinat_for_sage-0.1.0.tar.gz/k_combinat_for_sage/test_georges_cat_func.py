#!/usr/bin/env sage
# use `sage --python -m pdb test_all.py` for the debugger
# A place to test my functions
from __future__ import print_function
import time

from sage.all import *
print('Sage loaded.  Now loading local modules...')
from testing import *
from all import *
from strong_marked_tableau import __go_to_ribbon_head
from shorthands import *
start_time = time.time()
print('Modules loaded.  Testing...')



R = QQ['t']
t = R.gen()
K = FractionField(R)
Symt = SymmetricFunctions(K)
P = Symt.hall_littlewood().P()
Q = Symt.hall_littlewood().Q()
Qp = Symt.hall_littlewood().Qp()
s = Symt.schur()
h = Symt.h()
m = Symt.m()
p = Symt.p()
ROA = RaisingOperatorAlgebra(K)

def H(parti): # Jing operator
    if len(parti) == 0:
        return s[0]
    res = Qp([])
    for part in reversed(parti):
        if part < 0:
            return 0
        else:
            res = res.hl_creation_operator([part])
    return res

def delta_plus(n):
    return Set((i,j) for j in range(n) for i in range(j))

def rop(ideal,n,base_ring=K):
    t = base_ring.gen()
    roa = RaisingOperatorAlgebra(base_ring)
    deltaPlus = delta_plus(n)
    op_ideal = deltaPlus.difference(ideal)
    return reduce(lambda x,y: x*y, [(1-t*roa.ij(i,j)) for (i,j) in op_ideal],roa.one())

def catalan_fn(ideal,part,base_ring=K):
    n = len(part)
    rop_expr = rop(ideal,n,base_ring)
    res_parts = rop_expr(part)
    terms = [coeff*H(par) for (par,coeff) in res_parts]
    return Qp(sum(terms))

a(s(catalan_fn([],[2, 2, 1,1])), s[2, 2, 1, 1])












# ALL DONE!
print('Testing completed successfully!', end='')
end_time = time.time()
elapsed_time = end_time - start_time
print(' Elapsed time = {}'.format(elapsed_time))
