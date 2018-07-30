# coding:utf-8
from __future__ import print_function
from setuptools import setup,find_packages
import sys

setup(
    name="fancaiji",
    version="0.0.1",
    author="Edwin yang",
    author_email="yangyong@findourlove.com",
    description="fancaiji",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/",
    packages=['fancaiji-edwin'],
    install_requires=[
        "readability",
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
    ],

)