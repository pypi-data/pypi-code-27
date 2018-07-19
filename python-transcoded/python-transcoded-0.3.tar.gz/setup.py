#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='python-transcoded',
      version='0.3',
      description='Daemon for transcoding audio/video with an http API written in python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      license='MIT',
      url='https://gitlab.com/MartijnBraam/python-transcoded',
      packages=['transcoded'],
      python_requires='>=3',
      install_requires=['Werkzeug', 'requests'],
      classifiers=(
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Intended Audience :: System Administrators",
          "Topic :: Multimedia :: Video :: Conversion"
      ),
      project_urls={
          'Tracker': 'https://gitlab.com/MartijnBraam/python-transcoded/issues',
          'Documentation': 'https://python-transcoded.readthedocs.io/en/latest/'
      },
      package_data={
          'transcoded': ['example-config.ini']
      },
      entry_points={
          'console_scripts': [
              'transcoded=transcoded.__main__:main'
          ]
      }
      )
