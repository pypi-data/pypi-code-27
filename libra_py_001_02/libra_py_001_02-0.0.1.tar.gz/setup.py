#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 12:24:25 2018

@author: sxwxiaoxiao
"""

from setuptools import setup  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='libra_py_001_02',
    version='0.0.1',
    description='Split Linearized Bregman Iteration',
    long_description=long_description,
    url='https://github.com/tansey/smoothfdr',
    author='Xinwei Sun',
    author_email='sxwxiaoxiaohehe@pku.edu.cn',
    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='sparsity regularization path Lasso variable-selection',

    packages=['libra_py_001_02'],
    package_dir={'libra_py_001_02': 'libra_py_001_02'},
    install_requires=[
              'numpy',
              'scipy', 
              'matplotlib', 
              'scikit-learn'],
   
)
