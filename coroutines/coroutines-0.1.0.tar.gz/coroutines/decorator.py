
# all glory for this decorator belongs to David Beazley.
# https://www.dabeaz.com/coroutines/coroutine.py

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.__next__()
        return cr
    return start
