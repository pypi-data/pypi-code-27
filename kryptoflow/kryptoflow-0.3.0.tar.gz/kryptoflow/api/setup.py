#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for kryptoflow_serving.

    This file was generated with PyScaffold 3.0.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: http://pyscaffold.org/
"""

import sys
from setuptools import setup, find_packages

# Add here console scripts and other entry points in ini-style format
entry_points = """
[console_scripts]
# script_name = kryptoflow_serving.module:function
# For example:
# fibonacci = kryptoflow_serving.skeleton:run
"""


def setup_package():
    setup(entry_points=entry_points,
          version='0.12',
          tests_require=['pytest', 'pytest-cov', 'pytest-runner'],
          packages=find_packages(exclude=['docs', 'tests'], include=['kryptoflow_serving']))


if __name__ == "__main__":
    setup_package()
