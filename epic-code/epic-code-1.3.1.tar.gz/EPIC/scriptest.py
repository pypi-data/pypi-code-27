import multiprocessing

def f(*args):
    print(*args, sum(args))

if __name__ == '__main__':
    #multiprocessing.freeze_support()

    man = multiprocessing.Manager()
    m = man.list([1, 4, 6])

    proc = multiprocessing.Process(
            target=f,
            args=[4, 2, 7, 8],
            )

    proc.start()
    proc.join()

    proc2 = multiprocessing.Process(
            target=f,
            args=m,
            )
    proc2.start()
    proc2.join()

