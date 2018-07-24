#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='FAIRtools',
    version='0.1.0',
    description="FAIR Metrics Evaluation Tool",
    long_description=readme + '\n\n',
    author="Mario Prieto",
    author_email='mario.prieto@upm.es',
    url='https://github.com/wilkinsonlab/FAIRtools',
    packages=[
        'FAIRtools',
    ],
    package_dir={'FAIRtools':
                 'FAIRtools'},
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='FAIRtools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    install_requires=requirements,
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
