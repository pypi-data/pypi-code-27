#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.buffer',
  description = 'Facilities to do with buffers, primarily CornuCopyBuffer, an automatically refilling buffer intended to support parsing of data streams.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20180726',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3'],
  keywords = ['python3'],
  long_description = "\n\n## Function `chunky(bfr_func)`\n\nDecorator for a function acceptig a leading CornuCopyBuffer parameter.\nReturns a function accepting a leading data `chunks` parameter\nand optional `offset` and 'copy_offsets` keywords parameters.\n\n@chunky\ndef func(bfr, ...):",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.buffer'],
)
