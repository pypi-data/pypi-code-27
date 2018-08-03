#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SSHLitebrary',
    version="0.1",
    description='SSH and SFTP library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Leon Seng',    
    author_email="octleons@gmail.com",
    url="https://gitlab.com/octleons/SSHLitebrary",
    platforms='any',
    install_requires = ['paramiko'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
