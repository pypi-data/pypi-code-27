#!/usr/bin/env python

import os

from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="podop",
    version="0.2.2",
    description="Postfix and Dovecot proxy",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Pierre Jaury",
    author_email="pierre@jaury.eu",
    url="https://github.com/mailu/podop.git",
    packages=["podop"],
    include_package_data=True,
    scripts=["scripts/podop"],
    install_requires=[
        "aiohttp"
    ]
)
