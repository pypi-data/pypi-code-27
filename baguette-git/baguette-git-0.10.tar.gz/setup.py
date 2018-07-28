#-*- coding:utf-8 -*-
"""
Setup for baguette git package.
"""
from setuptools import find_packages, setup

setup(
    name='baguette-git',
    version='0.10',
    url='https://www.baguette.io',
    author_email='pydavid@baguette.io',
    packages=find_packages(),
    platforms=[
        'Linux/UNIX',
        'MacOS',
        'Windows'
    ],
    install_requires=[
        'baguette-messaging',
        'baguette-olite',
    ],
    extras_require={
        'testing': [
            'baguette-messaging[testing]',
            'pycrypto==2.6.1',
        ],
        'doc': [
            'Sphinx',
        ],
    },
    package_data={
        'frasage.tests': ['farine.ini', 'pytest.ini'],
    },
)
