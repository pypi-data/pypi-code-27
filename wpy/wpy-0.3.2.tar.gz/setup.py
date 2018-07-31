#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from setuptools import setup, find_packages

setup(
    name = 'wpy',
    version = '0.3.2',
    keywords='python3',
    description = 'a library for python Developer',
    license = 'MIT License',
    url = 'https://github.com/wxnacy/wpy',
    author = 'wxnacy',
    author_email = 'wxnacy@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests>=2.19.1',
        'pycrypto>=2.6.1',
        'Pillow>=5.2.0',
    ],
)

