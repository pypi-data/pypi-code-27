from .control import fmap
from .function import identity, Function


class Always(Function):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


class Switch(Function):
    def __init__(self, cond, f_true, f_false=identity):
        self.cond = cond
        self.f_true = f_true
        self.f_false = f_false

    def __call__(self, x):
        return self.f_true(x) if self.cond(x) else self.f_false(x)


def map_if(f_true, xs, cond, f_false=identity):
    return fmap(Switch(cond, f_true, f_false), xs)

def filterM(f, xs):
    ...

def decrease(fst, snd):
    return snd <= fst

def increase(fst, snd):
    return snd >= fst
