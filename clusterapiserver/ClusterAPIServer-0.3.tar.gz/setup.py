#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='ClusterAPIServer',
      version='0.3',
      author='Xin Liang',
      author_email='XLiang@suse.com',
      packages=find_packages(),
      install_requires=['Flask', 'xmltodict', 'PyJWT', 'python-pam'])
