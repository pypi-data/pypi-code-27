# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

VERSION = '0.3.1'

setup(
    name='kamonohashi-sdk',
    version=VERSION,
    description='KAMONOHASHI SDK for Python',
    long_description='Python client SDK for KAMONOHASHI https://kamonohashi.ai/',
    author='NS Solutions Corporation',
    author_email='kamonohashi-support@jp.nssol.nssmc.com',
    url='https://github.com/KAMONOHASHI/kamonohashi-sdk',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'urllib3 >= 1.15', 
        'six >= 1.10', 
        'certifi', 
    ]
)
