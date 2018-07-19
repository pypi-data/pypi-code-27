#!/usr/bin/env python3

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jclib",
    version="0.0.1",
    author="Joel Cross",
    author_email="joel@kazbak.co.uk",
    description="Reusable code",
    long_description=long_description,
    url="https://github.com/ukch/jclib",
    packages=["jclib"],
    license="MIT",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ),
)
