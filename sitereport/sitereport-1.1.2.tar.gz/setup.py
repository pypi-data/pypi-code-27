#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os
version = '1.1.2'
setup(name='sitereport',
      version=version,
      description=u'sitereport.cn api',
      long_description=open('README.rst').read(),
      classifiers=[],
      author='simon',
      author_email='simon@yesiming.com',
      url='https://www.sitereport.cn',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'pycurl',
        'demjson'
      ]
)
