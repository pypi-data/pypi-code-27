#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.ansi_colour',
  description = 'Convenience functions for ANSI terminal colour sequences',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20180725.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Development Status :: 6 - Mature', 'Environment :: Console', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Terminals', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Mapping and function for adding ANSI terminal colour escape sequences\nto strings for colour highlighting of output.\n\n## Function `colourise(s, colour=None, uncolour=\'normal\')`\n\nReturn a string enclosed in colour-on and colour-off ANSI sequences.  \n`colour` names the desired ANSI colour.  \n`uncolour` may be used to specify the colour-off colour;  \n  the default is \'normal\'.\n\n## Function `colourise_patterns(s, patterns, default_colour=None)`\n\nColourise a string according to regular expressions.  \n`s`: the string  \n`patterns`: a sequence of patterns  \n`default_colour`: if a string pattern has no colon, or starts  \n  with a colon, use this colour; default DEFAULT_HIGHLIGHT  \nEach pattern may be:  \n  a string of the form "[colour]:regexp"  \n  a string containing no colon, taken to be a regexp  \n  a tuple of the form (colour, regexp)  \n  a regexp object  \nReturns the string with ANSI colour escapes embedded.\n\n## Function `make_pattern(pattern, default_colour=None)`\n\nConvert a pattern specification into a (colour, regexp) tuple.  \nEach pattern may be:  \n  a string of the form "[colour]:regexp"  \n  a string containing no colon, taken to be a regexp  \n  a tuple of the form (colour, regexp)  \n  a regexp object\n\n## Function `make_patterns(patterns, default_colour=None)`\n\nConvert an iterable of pattern specifications into a list of (colour, regexp) tuples.  \nEach pattern may be:  \n  a string of the form "[colour]:regexp"  \n  a string containing no colon, taken to be a regexp  \n  a tuple of the form (colour, regexp)  \n  a regexp object',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.ansi_colour'],
)
