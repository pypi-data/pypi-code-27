#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
try:  # For pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # For pip <= 9
    from pip.req import parse_requirements


__version__ = '0.0.2'  # Should match with __init.py__
_GITHUB_URL = 'https://github.com/tducret/precisionmapper-python'
_KEYWORDS = ['api', 'precisionmapper', 'parsing', 'drone', 'platform',
             'python-wrapper', 'scraping', 'scraper', 'parser',
             'precisionhawk']


install_reqs = parse_requirements('requirements.txt', session='hack')
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name='precisionmapper',
    packages=find_packages(),
    package_data={},
    version=__version__,
    license="MIT license",
    platforms='Posix; MacOS X',
    description="Python package to communicate with precisionmapper.com",
    long_description="Python package to communicate with precisionmapper.com",
    author="Thibault Ducret",
    author_email='hello@tducret.com',
    url=_GITHUB_URL,
    download_url='%s/tarball/%s' % (_GITHUB_URL, __version__),
    keywords=_KEYWORDS,
    setup_requires=requirements,
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    tests_require=['pytest'],
)

# ------------------------------------------
# To upload a new version on pypi
# ------------------------------------------
# Make sure everything was pushed (with a git status)
# (or git commit --am "Comment" and git push)
# export VERSION="0.0.2"; git tag $VERSION -m "Added id and url"; git push --tags

# If you need to delete a tag
# git push --delete origin $VERSION; git tag -d $VERSION
