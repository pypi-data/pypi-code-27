


def trivialProducer(s,ncr):
    while True:
        ncr.send(s)

def cycleProducer(s,ncr):
    while True:
        for e in s:
            ncr.send(e)

def fileproducer(fname,ncr):
    with open(fname) as f:
        for line in f:
            ncr.send(line)

def finiteProducer(n,ncr):
    for i in range(n):
        ncr.send(i)
