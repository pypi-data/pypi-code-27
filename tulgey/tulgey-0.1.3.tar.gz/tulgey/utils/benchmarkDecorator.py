import logging
from time import time

def benchmark(f):
    def benchmarked_f(*args, **kwargs):
        startTime = time()
        res = f(*args, **kwargs)
        timeToRun = time() - startTime
        logging.info("Took %s seconds to run %s.%s" % (str(timeToRun), f.__module__, f.__name__))
        return res
    return benchmarked_f
