#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.buffer',
  description = 'Facilities to do with buffers, primarily CornuCopyBuffer, an automatically refilling buffer to support parsing of data streams.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20180805',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.py3'],
  keywords = ['python3'],
  long_description = "Facilities to do with buffers, primarily CornuCopyBuffer, an automatically refilling buffer to support parsing of data streams.\n\n\n\n## Function `chunky(bfr_func)`\n\nDecorator for a function accepting a leading CornuCopyBuffer\nparameter.\nReturns a function accepting a leading data chunks parameter\n(bytes instances) and optional `offset` and 'copy_offsets`\nkeywords parameters.\n\nExample::\n\n  @chunky\n  def func(bfr, ...):\n\n## Class `CopyingIterator`\n\nWrapper for an iterator that copies every item retrieved to a callable.\n  \n\n## Class `CornuCopyBuffer`\n\nAn automatically refilling buffer intended to support parsing\nof data streams.\n\nAttributes:\n* `buf`: a buffer of unparsed data from the input, available\n  for direct inspection by parsers\n* `offset`: the logical offset of the buffer; this excludes\n  unconsumed input data and `.buf`\n\nThe primary methods supporting parsing of data streams are\nextend() and take(). Calling `.extend(min_size)` arranges\nthat `.buf` contains at least `min_size` bytes.  Calling `.take(size)`\nfetches exactly `size` bytes from `.buf` and the input source if\nnecessary and returns them, adjusting `.buf`.\n\nlen(CornuCopyBuffer) returns the length of `.buf`.\n\nbool(CornuCopyBuffer) tests whether len() > 0.\n\nIndexing a CornuCopyBuffer accesses `.buf`.\n\nA CornuCopyBuffer is also iterable, yielding data in whatever\nsizes come from its `input_data` source, preceeded by the\ncurrent `.buf` if not empty.\n\nA CornuCopyBuffer also supports the file methods `.read`,\n`.tell` and `.seek` supporting drop in use of the buffer in\nmany file contexts. Backward seeks are not supported. `.seek`\nwill take advantage of the `input_data`'s .seek method if it\nhas one, otherwise it will use reads.\n\n## Class `SeekableFDIterator`\n\nAn iterator over the data of a file descriptor.\n  \n\n## Class `SeekableFileIterator`\n\nAn iterator over the data of a file object.\n  ",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.buffer'],
)
