import time
import pandas as pd
from functools import wraps
from itertools import islice, chain


def inverse_map(x, freeze_values=False):
    inv = {}
    for k, v in x.items():
        inv.setdefault(v, set()).add(k)
    if freeze_values:
        for k, v in inv.items():
            inv[k] = frozenset(v)
    return inv


def split_every(iterable, size=None):
    iterator = iter(iterable)
    while True:
        slice_iter = islice(iterator, size)
        peek = next(slice_iter)
        yield chain([peek], slice_iter)


def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (f.__name__, args, kw, te-ts))
        return result
    return wrap


def import_from_xlsx(con, filename):
    wb = pd.read_excel(filename, sheetname=None)
    for sheet in wb:
        wb[sheet].to_sql(sheet, con, index=False)


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def list_default(l, index, default_value):
    try:
        return l[index]
    except IndexError:
        return default_value


def list_default2(l, index, default_value):
    return (l[index:] + [default_value])[0]
