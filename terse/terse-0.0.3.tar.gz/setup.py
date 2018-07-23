#!/usr/bin/env python3
from setuptools import setup, find_packages
from os import path
proj_path = path.abspath(path.dirname(__file__))
md_path = path.join(proj_path, 'README.md')

with open(md_path) as f:
    long_description = f.read()

setup(
    author='Chad Lucas',
    author_email='cjlucas85@gmail.com',
    description='a collection of function decorators to handle common procedures done on the entry and exit points.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    name='terse',
    url='https://github.com/cjlucas85/terse',
    version='0.0.3',
    packages=find_packages(),
)
