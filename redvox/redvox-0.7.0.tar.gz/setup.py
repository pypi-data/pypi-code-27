from setuptools import setup, find_packages

setup(name='redvox',
    version='0.7.0',
    url='https://bitbucket.org/redvoxhi/redvox-api900-python-reader/src/master/',
    license='Apache',
    author='RedVox',
    author_email='dev@redvoxsound.com',
    description='Library for working with RedVox files.',
    packages=find_packages(include=["redvox", "redvox.api900", "redvox.api900.lib"], exclude=['tests']),
    long_description=open('README.md').read(),
    install_requirements=["lz4", "numpy", "protobuf"],
    zip_safe=False)
