import sys
from .cli import reference, execute, modules

if sys.argv[1] == 'reference':
    reference.handler(sys.argv[2:])
elif sys.argv[1] == 'modules':
    modules.handler(sys.argv[2:])
else:
    execute.handler()
