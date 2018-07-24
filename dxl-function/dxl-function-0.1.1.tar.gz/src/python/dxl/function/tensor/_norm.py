import numpy as np
from functools import singledispatch
from dxl.data.tensor import Point


@singledispatch
def norm(t, *, p=2.0):
    return np.linalg.norm(t)


@norm.register(np.ndarray)
def _(t, *, p=2.0):
    return np.linalg.norm(t)


@norm.register(np.ndarray)
def _(t, *, p=2.0):
    return norm(t.data)


@norm.register(list)
def _(t, *, p=2.0):
    return norm(np.array(t))
