#!/usr/bin/env python
#:coding=utf-8:

import os
from setuptools import setup, find_packages

def read_file(filename):
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, filename)
    with open(filepath) as f:
        read_text = f.read()
    return read_text


setup(
    name='bpnotify',
    version='0.46',
    description='Notification routing for Django',
    author='BeProud',
    author_email='project@beproud.jp',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/beproud/bpnotify/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    test_suite='tests.main',
    install_requires=[
        'Django>=1.8',
        'django-jsonfield>=1.0.1',
        'six',
    ],
    tests_require=[
        'celery>=4.1',
        'mock>=0.7.2',
    ],
    zip_safe=False,
)
