import logging
from time import time

def short_str(any) -> str:
    s = str(any)
    if len(s) < 20:
        return s
    else:
        return s[:10] + " ... " + s[-10:]

def benchmark(f):
    def benchmarked_f(*args, **kwargs):
        startTime = time()
        res = f(*args, **kwargs)
        timeToRun = time() - startTime
        args = [short_str(x) for x in args]
        argStr = ", ".join(args) + ", " + ", ".join([key + "=" + str(val) for key, val in kwargs.items()])
        logging.info("Took %s seconds to run %s.%s(%s)" % (str(timeToRun), f.__module__, f.__name__, argStr))
        return res
    return benchmarked_f
