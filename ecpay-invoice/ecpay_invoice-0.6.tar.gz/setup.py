#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import io

VERSION = '0.6'

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

install_requires = open("requirements.txt").readlines()

setup(
    name="ecpay_invoice",
    version=VERSION,
    author="Hiskyz",
    author_email="skypc785308@gmail.com",
    url="https://github.com/skypc785308/ecpay_invoice",
    description="ecpay_invoice",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=install_requires,
)
