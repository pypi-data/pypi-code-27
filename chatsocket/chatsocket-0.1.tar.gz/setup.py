# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='chatsocket',
    version='0.1',
    description='This is a websocket chat',
    long_description=long_description,
    url='http://github.com/storborg/funniest',
    author='Kevin, Michael',
    author_email='123kangpeng@gmail.com',
    license='None',
    packages=['chatsocket'],
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)

