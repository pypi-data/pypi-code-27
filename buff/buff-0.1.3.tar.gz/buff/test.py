#!/usr/bin/env python

from buff import Datatype, Union
u = Union()
d = Datatype(4, 's')
print(u.unpack_odd('\xf0', d))
