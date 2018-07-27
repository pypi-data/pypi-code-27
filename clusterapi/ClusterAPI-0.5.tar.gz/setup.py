#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='ClusterAPI',
      version='0.5',
      author='Xin Liang',
      author_email='XLiang@suse.com',
      packages=find_packages(),
      scripts=['bin/clusterAPIServer'],
      install_requires=['Flask', 'xmltodict', 'PyJWT', 'python-pam'])
