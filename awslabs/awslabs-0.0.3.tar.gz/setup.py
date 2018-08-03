# -*- coding: utf-8 -*-


'''setup.py: setuptools control.'''


import re
import setuptools
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), 'r') as f:
    long_description = f.read()

version = "0.0.3"

setuptools.setup(
    name='awslabs',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['awslabs = awslabs.awslabs:main']
    },
    version=version,
    description='This cli contains aws labs to try.',
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['boto3', 'requests', 'configparser', 'click', 'cfn_flip', 'pylint'],
    author='Martijn van Dongen',
    author_email='martijnvandongen@binx.io',
    url='https://github.com/binxio/awslabs',
)