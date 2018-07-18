#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "thinkutils_plus",
    version = "0.0.1",
    keywords = ("pip", "thinkman","thinkutils"),
    description = "Thinkman's thinkutils",
    long_description = "Thinkman's thinkutils",
    license = "MIT Licence",

    url = "https://github.com/ThinkmanWang/thinkutils_plus",
    author = "Thinkman",
    author_email = "wangxf1985@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["redis", "tornado==4.4.3", "M2Crypto", "logutils"]
)