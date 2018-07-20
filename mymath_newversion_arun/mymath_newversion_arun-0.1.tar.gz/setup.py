#!/usr/bin/env python

from setuptools import setup


# This setup is suitable for "python setup.py develop".

setup(name='mymath_newversion_arun',
      version='0.1',
      description='A silly math package',
      author='Arunansu Gorai',
      author_email='chi.square.revisted@gmail.com',
      url='http://www.mymath.org/',
      packages=['mymath', 'mymath.adv'],
      )