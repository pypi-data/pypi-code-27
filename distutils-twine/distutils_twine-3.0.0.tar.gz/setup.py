#!/usr/bin/env python3

import setuptools
from distutils_twine import release

setuptools.setup(cmdclass={"release": release})
