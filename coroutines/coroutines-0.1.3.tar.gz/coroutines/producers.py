


def trivialProducer(s,ncr):
    try:
        while True:
            ncr.send(s)
    except StopIteration:
        pass

def cycleProducer(s,ncr):
    try:
        while True:
            for e in s:
                ncr.send(e)
    except StopIteration:
        pass

def fileproducer(fname,ncr):
    try:
        with open(fname) as f:
            for line in f:
                ncr.send(line)
    except StopIteration:
        pass

def finiteProducer(n,ncr):
    try:
        for i in range(n):
            ncr.send(i)
    except StopIteration:
        pass
