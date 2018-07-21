# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import codecs
import os
import ubindex

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_desc = """

UBIndex
===============


Install
--------------

    pip install ubindex
    
Upgrade
---------------

    pip install ubindex --upgrade
    
    
"""


setup(
    name='ubindex',
    version=ubindex.__version__,
    description='UB Crypto Asset Indices',
#     long_description=read("READM.rst"),
    long_description = long_desc,
    author='tushare.org',
    author_email='waditu@163.com',
    license='Apache 2.0',
    url='http://tushare.org',
    keywords='Crypto Asset Index',
    classifiers=['Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: BSD License'],
    packages=find_packages(),
    package_data={'': ['*.csv']},
)