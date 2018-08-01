# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 13:21
# @Author  : yangyong
# @Email   : yangyong@findourlove.com
# @File    : setup.py
# @Software: PyCharm
from __future__ import print_function
from setuptools import setup,find_packages
import sys

setup(
    name="extensive_collection",
    version="0.0.5",
    author="Edwin yang",
    author_email="yangyong@findourlove.com",
    description="extensive_collection",
    long_description=open("README.rst").read(),
    license="MIT",
    packages=['extensive_collection','extensive_collection/compat'],
    install_requires=[
        "pandas",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],

)