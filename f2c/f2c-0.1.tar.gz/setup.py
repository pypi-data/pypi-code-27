'''
Created on Aug 1, 2018

@author: josh.bregman
'''
from setuptools import setup, find_packages



setup(
  name = 'f2c',
  packages=find_packages(),
  version = '0.1',
  description = 'Configuration utility for CyGlass Fortigate Integration',
  author = 'Josh Bregman',
  author_email = 'josh.bregman@cyglass.com',
  url = 'https://github.com/CyGlass/fortinet-cyglass', 
#  download_url = 'https://github.com/CyGlass/fortinet-cyglass', 
  keywords = ['fortigate', 'cyglass', 'network'],
  classifiers = [],
  install_requires=['FortigateApi'],
  entry_points = {
        'console_scripts': ['f2c=cyglass.f2c.__main__:main'],
  }

)