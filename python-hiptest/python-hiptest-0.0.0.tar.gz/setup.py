"""setup.py

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from setuptools import setup
from hiptest import __author__, __email__, __license__, __version__


setup(name='python-hiptest',
      version=__version__,
      description='Unofficial python API client for Hiptest',
      author=__author__,
      author_email=__email__,
      url=u'https://github.com/jlane9/python-hiptest',
      packages=['hiptest'],
      install_requires=[''],
      keywords='hiptest qa testing bdd api',
      license=__license__,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ])
