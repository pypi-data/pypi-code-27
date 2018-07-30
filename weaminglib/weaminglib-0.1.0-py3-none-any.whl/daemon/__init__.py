import time


def loop(fn, seconds, args=(), kwargs={}):
    while 1:
        if fn and callable(fn):
            fn(*args, **kwargs)
        if seconds and seconds > 0:
            time.sleep(seconds)


def block(seconds):
    loop(None, seconds)


def map_do(fn, n):
    from multiprocessing.pool import Pool
    p = Pool()

    def f(i):
        fn(i)

    p.map(f, range(1, n + 1))
