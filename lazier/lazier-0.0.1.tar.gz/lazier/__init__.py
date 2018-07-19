name = "lazier"


import functools
def lazier(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
            inner.kwargs.update(kwargs)
            inner.args = args if len(args) !=0 else inner.args
            try:
                return f(*inner.args, **inner.kwargs)
            except TypeError as e:
                print(e)

    def reset():
        inner.kwargs = {}
        inner.args = ()
        
    inner.reset = reset
    
    inner.reset()
    return inner