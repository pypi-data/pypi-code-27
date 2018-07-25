# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

setup_requires = ['pytest-runner', 'pytest']

with open('./fama/_version.py') as f:
    __version__ = re.search(r"__version__?\s=?\s'([^']+)", f.read()).groups()[0]

with open('./requirements.txt') as f:
    requirements = [req.strip() for req in f.readlines() if req]

setup(
    name='latte-fama',
    version=__version__,
    author="Diana Spencer, Miles Granger",
    maintainer="Miles Granger, Diana Spencer",
    keywords="report bi business intelligence",
    url="https://github.com/milesgranger/latte-fama",
    description="Automated report tooling",
    long_description= \
        """"
        Automated report tooling
        """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=requirements,
    test_suite='tests',
    setup_requires=setup_requires + requirements,
    include_package_data=True,
    zip_safe=True
)
