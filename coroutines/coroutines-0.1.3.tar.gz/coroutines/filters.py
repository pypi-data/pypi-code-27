from .decorator import coroutine
import re
from collections import deque

@coroutine
def split(ncr1,ncr2):
    try:
        while True:
            s = yield
            ncr1.send(s)
            ncr2.send(s)
    except StopIteration:
        pass


class combine():
    def __init__(self,n,ncr):
        self.q = [ deque() for i in range(n)]
        self.n = n
        self.x = 0
        self.ncr = ncr

    @coroutine
    def receiver(self,n):
        assert n < self.n
        try:
            while True:
                s = (yield)
                self.q[n].append(s)
                while True:
                    if self.q[self.x]:
                        self.ncr.send(self.q[self.x].popleft())
                        self.x = (self.x + 1) % self.n
                    else:
                        break
        except StopIteration:
            pass

@coroutine
def matchre(regex,ncrmatch,ncrnomatch):
    m=re.compile(regex)
    try:
        while True:
            s = yield
            res = m.match(s)
            if res and ncrmatch:
                ncrmatch.send(s)
            if not res and ncrnomatch:
                ncrnomatch.send(s)
    except StopIteration:
        pass
