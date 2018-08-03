# -*- encoding: utf-8
"""
Like subprocess, but better.
"""

import subprocess
import sys


def call(*args):
    print('*** Running command %r' % ' '.join(args))
    return subprocess.call(args)


def check_call(*args):
    print('*** Running command %r' % ' '.join(args))
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as err:
        sys.exit(err.exitcode)


def check_output(*args):
    print('*** Running command %r' % ' '.join(args))
    try:
        return subprocess.check_output(args).decode('utf8').strip()
    except subprocess.CalledProcessError as err:
        sys.exit(err.exitcode)
