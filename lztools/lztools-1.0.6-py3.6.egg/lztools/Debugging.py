import inspect
import gc

import time
from sys import maxsize

def get_variable_name():
    f = inspect.currentframe().f_back.f_back
    filename = inspect.getfile(f)
    code_line = open(filename).readlines()[f.f_lineno - 1]
    assigned_variable = code_line.split("=")[0].strip()
    return assigned_variable

def find_names(self):
    frame = inspect.currentframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    obj_names = []
    for referrer in gc.get_referrers(self):
        if isinstance(referrer, dict):
            for k, v in referrer.items():
                if v is self:
                    obj_names.append(k)
    print(obj_names)

def _time_operation(func):
    t1 = time.time()
    func()
    return time.time() - t1

def time_operation(func, count, id=None):
    if id is None:
        id=""
    else:
        id = "{}: ".format(id)
    total = 0
    min = maxsize
    max = 0
    for i in range(1, count+1):
        t = _time_operation(func)
        total += t
        if t > max:
            max = t
        if t < min:
            min = t
        average = total / i
        if i % 50 == 0:
            print("{}#{}: Average: {}\tMin: {}\tMax: {}".format(id, i, average, min, max))