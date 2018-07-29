# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(name='pyTemplePriest',
      version='0.1',
      description='Python temple priest api. ',
      long_description=readme(),
      author='painca',
      author_email='painca@tutanota.com',
      url='https://github.com/painca/pyTemplePriestAPI',
      packages=['templepriest'],
      license='GPL3',
      install_requires=['requests'],
      )
