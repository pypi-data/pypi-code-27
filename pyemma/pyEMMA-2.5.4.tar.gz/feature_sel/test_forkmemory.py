#!/usr/bin/env python

import numpy as np

x = np.zeros(int(512 * 1024** 2 / 8))
x.flags.writeable = False
print('mem size in mb:', x.nbytes / 1024**2)

def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        print('%-10s : %7s' % (name.capitalize(), value))


def func(i):
    print(i, x.__array_interface__['data'][0])
    #print(id(x))

if __name__ == '__main__':
    # 0.5 GB in data
    n = 2
    import psutil
    from multiprocess import Pool
    parent = psutil.Process()
    print(parent, pprint_ntuple(parent.memory_full_info()))
    import gc, subprocess
    gc.collect()
    with Pool(n) as p:
        tasks = [p.apply_async(func, [i] ) for i in range(n)]
        [t.get() for t in tasks]
        children = parent.children(recursive=True)
        for c in children:
            print(c, pprint_ntuple(c.memory_full_info()))
            #print(subprocess.check_output(['cat', '/proc/{id}/meminfo'.format(id=c.pid)]))

    #for i in range(n):
    #    assert x[i] == i, i
