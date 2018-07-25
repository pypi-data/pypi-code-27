#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.x',
  description = 'X(), for low level debugging',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20180726',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'X() is my function for low level ad hoc debug messages.\nIt takes a message and optional format arguments for use with `%`.\nIt is presented here in its own module for reuse.\n\nIt normally writes directly to `sys.stderr` but accepts an optional\nkeyword argument `file` to specify a different filelike object.\nIf `file` is not specified, its behaviour is further tweaked with\nthe globals `X_logger` or `X_via_tty`:\nif X_logger then log a warning to that logger;\notherwise, if X_via_tty then open /dev/tty and write the message to it;\notherwise, write the message to sys.stderr.\n\n## Function `X(msg, *args, **kw)`\n\nUnconditionally write the message `msg`.\n\n* `args`: if not empty, format `msg` using %-expansion with `args`.\n* `file`: optional keyword argument specifying the output file.\n\nIf `file` is not None, write to it unconditionally;\notherwise, if X_logger then log a warning to that logger;\notherwise, if X_via_tty then open /dev/tty and write the message to it;\notherwise write the message to sys.stderr.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.x'],
)
