#! /usr/bin/python

from setuptools import setup, find_packages

# import os
# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# version_path = os.path.join(THIS_FOLDER,'VERSION')
# require_path = os.path.join(THIS_FOLDER, 'requirements.txt')


with open('VERSION') as f:
      ada_core_version = f.read().strip()

with open('requirements.txt') as f:
      required = f.read().splitlines()

setup(name="ada_core",
      description='ada_core is an anomaly detection library for timeseries data',
      url='https://github.paypal.com/ROM/ada_core',
      author='Cai, Qianwen',
      author_email='cai.qianwen@hotmail.co.uk',
      version=ada_core_version,
      packages=['ada_core', 'ada_core.algorithms', 'ada_core.data_model'],
      install_requires=required,
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    )
      )
