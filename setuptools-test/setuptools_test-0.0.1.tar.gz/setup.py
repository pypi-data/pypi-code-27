from setuptools import setup, find_packages
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='setuptools_test',
    version='0.0.1',
    description='Testing packaging with Python 3',
    author='Sheel Dandekar',
    author_email='sheel_dandekar@intuit.com',
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)