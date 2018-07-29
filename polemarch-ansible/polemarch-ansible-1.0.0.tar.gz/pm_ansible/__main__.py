import sys
from .cli import reference, execute

if sys.argv[1] == 'reference':
    reference.handler(sys.argv[2:])
else:
    execute.handler()
