from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="datetimex",
    version="1.0.0",
    author="greenlotusx",
    author_email="greenlotusx@163.com",
    description="A Python library that formats strings with date and time.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/GreenLotusx/DateTimex",
    packages=['datetimex'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)