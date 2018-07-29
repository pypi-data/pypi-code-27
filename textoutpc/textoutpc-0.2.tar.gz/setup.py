#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the fingerd Python 3.x module, which is MIT-licensed.
#******************************************************************************
""" Setup script for the textoutpc Python package and script. """

from sphinx.setup_command import BuildDoc as _BuildDoc
from setuptools import setup as _setup

# Actually, most of the project's data is read from the `setup.cfg` file.

_setup(cmdclass = {'build_sphinx': _BuildDoc})

# End of file.
