# -*- coding: utf-8 -*-i
import numpy as np
def gkern(l=5, sig=1.):
    """
     creates gaussian kernel with side length l and a sigma of sig
   """
    if l%2 == 0:
        ax = np.arange(-l//2, l//2+1)
        ax = np.concatenate((ax[:l//2],ax[l//2+1:]))
    else:
        ax = np.arange(-l // 2 + 1., l // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sig**2))
    return kernel / np.sum(kernel)


print(gkern(10, 1))

import ipdb;ipdb.set_trace()
print(gkern(10,3))
