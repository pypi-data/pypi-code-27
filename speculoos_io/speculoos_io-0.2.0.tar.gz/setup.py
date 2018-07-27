# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:32:21 2016

@author: 
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""


from setuptools import setup

setup(
    name = 'speculoos_io',      # The name of the PyPI-package.
    packages = ['specio'],
    version = '0.2.0',    # Update the version number for new releases
    description = 'Wrapper for astropy and cfitsio readers for SPECULOOS data and log files',
    author = 'Maximilian N. Guenther',
    author_email = 'mg719@cam.ac.uk',
    url = 'https://github.com/MNGuenther/specio',
    download_url = 'https://github.com/MNGuenther/specio/releases',
    classifiers = [],
    install_requires=[],
    include_package_data = True
    )



