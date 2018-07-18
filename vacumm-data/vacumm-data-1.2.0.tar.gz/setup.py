# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup
import os
from vacumm_data import (__version__ as version,
                         __author__ as author,
                         __email__ as author_email,
                         __url__ as url,
                         )

data_files = []
for root, dirs, files in os.walk("share/vacumm", topdown=False):
    if files:
        files = [os.path.join(root, fname) for fname in files]
        data_files.append((root, files))

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(name='vacumm-data',
          version=version,
          description=('Data used by the vacumm python library '
                       'and its tutorials and tests'),
          long_description=long_description,
          author=author,
          author_email=author_email,
          url=url,
          py_modules=['vacumm_data'],
          data_files=data_files,
          classifiers=[
                       "Intended Audience :: Science/Research",
                       ("License :: OSI Approved :: CEA CNRS Inria Logiciel "
                       "Libre License, version 2.1 (CeCILL-2.1)"),
                       "Programming Language :: Python :: 2",
                       "Programming Language :: Python :: 3",
                       "Operating System :: OS Independent",
                       ]
          )
