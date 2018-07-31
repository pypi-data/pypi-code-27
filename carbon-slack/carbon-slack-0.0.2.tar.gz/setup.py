#!/usr/bin/env python2

from setuptools import setup, find_packages
import sys

with open('README.rst', 'r') as f:
  long_description=f.read()

version='0.0.2'

setup(
    zip_safe=True,
    name='carbon-slack',
    version=version,
    description="Use Slack as a bus for GraphiteDB / Carbon",
    long_description=long_description,
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Programming Language :: Python :: 2",
      "Topic :: Utilities",
    ],
    keywords='graphite carbon metrics monitoring slack',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/jdcasey/carbon-slack',
    license='GPLv3+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      "slackclient",
      "click",
      "ruamel.yaml"
    ],
    test_suite="tests",
    entry_points={
      'console_scripts': [
        'carbon-slack-init = carbon_slack:init',
        'carbon-slack-recv = carbon_slack:recv',
        'carbon-slack-relay = carbon_slack:relay',
        'carbon-slack-send = carbon_slack:send'
      ],
    }
)

