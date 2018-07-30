import logging
from time import time

def benchmark(f):
    def benchmarked_f(*args, **kwargs):
        startTime = time()
        res = f(*args, **kwargs)
        timeToRun = time() - startTime
        argStr = ", ".join(str(x) for x in args) + ", " + ", ".join([key + "=" + str(val) for key, val in kwargs.items()])
        logging.info("Took %s seconds to run %s.%s(%s)" % (str(timeToRun), f.__module__, f.__name__, argStr))
        return res
    return benchmarked_f
