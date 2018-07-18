#!/usr/bin/env python3

import setuptools
from distutils_twine import twineupload

setuptools.setup(cmdclass={"release": twineupload})
