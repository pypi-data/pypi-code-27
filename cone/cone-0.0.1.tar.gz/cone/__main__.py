import argparse
import sys

from .cone_test import test
from .cone_deploy import deploy
from .cone_revert import revert
from .cone_version import version

def main():
    pass

parser = argparse.ArgumentParser(
    usage='''cone <command>

Command list:
    test            Sends a request to test your code

    deploy          Updates your code to the Roblox place
     -t, --test     Sends your test files too

    revert          Reverts your last deployment

'''
)
parser.add_argument('command', help='command to run')
command = parser.parse_args(sys.argv[1:2]).command

if command == 'test':
    test(sys.argv[2:])
elif command == 'deploy':
    deploy(sys.argv[2:])
elif command == 'revert':
    revert(sys.argv[2:])
elif command == 'version':
    version()
else:
    parser.print_help()
