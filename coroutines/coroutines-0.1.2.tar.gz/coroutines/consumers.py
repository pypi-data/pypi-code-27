from .decorator import coroutine


@coroutine
def trivialConsumer():
    try:
        while True:
            s=yield
            print(s)
    except StopIteration:
        pass

@coroutine
def fileConsumer(fname, mode='w'):
    try:
        with open(fname,mode) as f:
                while True:
                    s=yield
                    f.write(s)
    except StopIteration:
        pass
