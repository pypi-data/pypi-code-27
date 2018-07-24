import numpy as np
from beluga.bvpsol.algorithms import Collocation
from beluga.bvpsol import Solution

def odefun(t, X, p, const):
    return 1 * p[0]

def bcfun(t0, X0, q0, tf, Xf, qf, p, aux):
    return (X0[0] - 0, Xf[0] - 2)


algo = Collocation()
solinit = Solution()
solinit.t = np.linspace(0, 1, 4)
solinit.y = np.array([[0], [0], [0], [0]])
solinit.parameters = np.array([1])
out = algo.solve(odefun, None, bcfun, solinit)
