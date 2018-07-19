#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(name='gorille',version="0.0.1",packages=find_packages(),author="Cyber-Detect",author_email="team@cyber-detect.com",license="Proprietary",

    # short description    
    description="The cyber-detect gorille module for ploting a 3D graph",
 
    # long description
    #long_description=open('README.md').read(),
 
    # requirements
    install_requires=["plotly"],
 
    # enable MANIFEST.in file parsing
    #include_package_data=True,
 
    # official lib url
    url='http://cyber-detect.eu/fr-produits-services-cybersecurite.html', 
 
    # plugins
    entry_points = {
        'console_scripts': [
            'sigplot = gorille.sigplot:main',
        ],
    },    
 
)
