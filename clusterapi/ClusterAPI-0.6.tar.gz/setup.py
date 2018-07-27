#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='ClusterAPI',
      version='0.6',
      author='Xin Liang',
      author_email='XLiang@suse.com',
      packages=find_packages(),
      scripts=['bin/clusterAPIServer'],
      install_requires=['Flask', 'flask_swagger','xmltodict', 'PyJWT', 'python-pam'])
