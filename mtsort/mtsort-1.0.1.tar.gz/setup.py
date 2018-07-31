#!/usr/bin/env python3

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mtsort',
    url='https://github.com/stiftcast/mtsort',
    author='stiftcast',
    author_email='stiftcast@gmail.com',
    version='1.0.1',
    license='MIT',
    description='A cross-platform module for sorting files by time.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['mtsort'],
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'mtsort = mtsort:main',
        ],
    }
)
