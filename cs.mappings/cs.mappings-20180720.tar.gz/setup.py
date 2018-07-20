#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.mappings',
  description = 'Facilities for mappings and objects associated with mappings.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20180720',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.sharedfile', 'cs.lex', 'cs.logutils', 'cs.py3', 'cs.seq'],
  keywords = ['python2', 'python3'],
  long_description = 'In particular:\n\n    - named_column_tuple(column_names), a function returning a factory\n        for namedtuples subclasses derived from the supplied column\n        names\n\n    - named_column_tuples(rows), a function returning a namedtuple\n        factory and an iterable of instances containing the row data\n\n    These are used by the csv_import and xl_import functions from cs.csvutils.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.mappings'],
)
