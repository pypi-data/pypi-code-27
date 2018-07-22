#!/usr/bin/env python

import os
from setuptools import setup

description = None

if os.path.exists('README.md'):
    with open('README.md') as fp:
        description = fp.read()

setup(
    name='gcdb',
    version='0.1.0',
    description=description,
    url='https://github.com/kylef/gcdb',
    author='Kyle Fuller',
    author_email='kyle@fuller.li',
    packages=('gcdb',),
    install_requires=('Click'),
    entry_points={
        'console_scripts': (
            'gcdb = gcdb:cli',
        )
    },
)

