#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(name='vulcan',
      version='0.1.3',
      description='Terminal-based flashcard application, for developers, that uses machine learning to schedule reviews',
      author='Shyal',
      author_email='shyal@shyal.com',
      url='https://www.github.com/shyal/vulcan/',
      packages=['vulcan', 'vulcan.lib'],
      scripts=['vulcan/vulcan'],
      install_requires=['urwid','sqlalchemy']
)

