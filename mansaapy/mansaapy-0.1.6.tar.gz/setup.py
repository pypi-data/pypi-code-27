#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings

dynamic_requires = []

version = '0.1.6'

setup(
    name='mansaapy',
    version='0.1.6',
    author='Kurien Zacharia',
    author_email='kurienzach@gmail.com',
    url='http://github.com/kurienzach/mansaapy',
    packages=find_packages(),
    scripts=[],
    description='Python API for controlling Mansaa Smartshine Bluetooth bulbs',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'bluepy==1.1.4',
    ],
    include_package_data=True,
    zip_safe=False,
)
