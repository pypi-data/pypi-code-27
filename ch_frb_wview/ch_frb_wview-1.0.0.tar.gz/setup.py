#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from setuptools import setup
from codecs import open
import glob

setup(
    name='ch_frb_wview',
    version='1.0.0',
    description='Web Application to operate the FRB L1 system.'
,

    author='Dustin Lang, Chitrang Patel',
    author_email='chitrang.patel@mail.mcgill.ca',
    url="https://github.com/CHIMEFRB/frb_monitoring.git",
    packages= ['ch_frb_wview'],
    scripts=['run-uwsgi.sh', 'run-webapp.sh'],
    include_package_data=True,
    install_requires=['flask',
                      'pyyaml',
                      'msgpack',
                      'numpy',
                      'sqlalchemy',
                      'passlib',
                      'zmq',
                      'scipy',
                      'requests',
                      'matplotlib']
)
