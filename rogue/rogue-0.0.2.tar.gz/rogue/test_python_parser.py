#!/usr/bin/env python
path = './test_python.py'
with open(path) as f:
    source = f.read()

import ast
a = ast.parse(source)
b = a.body
f = b[0]
c = compile(a, '', 'exec')
exec(c)
