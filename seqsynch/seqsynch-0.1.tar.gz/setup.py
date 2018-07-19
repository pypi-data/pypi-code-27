# -*- coding: utf-8 -*-
"""
@author: mezeda01
this is a setup file"""

from setuptools import setup

setup(name='seqsynch',
      version='0.1',
      description='GitHub synch for sequence management',
      url='https://github.com/medneo/protocol_management_github_ssh',
      author='David Mezey (mezdahun) @ Medneo',
      author_email='david.mezey@medneo.com',
      license='',
      packages=['seqsynch'],
      install_requires=[
          'schedule',
          'gitpython',
          'configparser',
      ],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['seqsynch-start=seqsynch.command_line:main'],
        },
      test_suite='nose.collector',
      tests_require=['nose'])
