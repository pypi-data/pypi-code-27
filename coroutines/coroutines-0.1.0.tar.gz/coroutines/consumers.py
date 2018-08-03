from .decorator import coroutine


@coroutine
def trivialConsumer():
    while True:
        s=yield
        print(s)


@coroutine
def fileConsumer(fname, mode='w'):
    with open(fname,mode) as f:
            while True:
                s=yield
                f.write(s)