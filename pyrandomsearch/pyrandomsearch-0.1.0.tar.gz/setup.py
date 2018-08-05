#!/usr/bin/env python3
from setuptools import find_packages, setup
import subprocess

proc = subprocess.Popen(
    ['git', 'describe', '--tags'],
    stdout=subprocess.PIPE,
    universal_newlines=True)
proc.wait()
if proc.returncode != 0:
    version = 'unknown'
else:
    version = proc.stdout.read().strip()

setup(
    name='pyrandomsearch',
    description='Command line utility to perform random search',
    author='Viet The Nguyen',
    author_email='vietjtnguyen@gmail.com',
    url='https://github.com/vietjtnguyen/pyrandomsearch/',
    # https://bit.ly/2LRjJBU
    version=version,
    packages=find_packages(),
    # https://bit.ly/2NX0Uur
    package_data={
    },
    # https://bit.ly/2Kd0X3j
    entry_points={
        'console_scripts': [
            'pyrandomsearch = pyrandomsearch.pyrandomsearch:main',
        ],
    },
    # https://bit.ly/2ArrmdZ
    install_requires=open('requirements.txt', 'r').readlines(),
    # https://bit.ly/2LCuB7w
    # https://bit.ly/2M4OU9O
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    test_suite='pyrandomsearch.test',
)
