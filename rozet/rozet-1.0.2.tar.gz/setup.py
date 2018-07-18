import os
from setuptools import setup, find_packages

datadir = os.path.join('rozet','abis')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup(
    name='rozet',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    data_files=datafiles,
    url='https://github.com/RozetProtocol/rozetPythonSdk',
    license='MIT',
    author='Rozet',
    author_email='dave@rozet.io',
    description='SDK for Rozet Smart Contracts',
    install_requires=[
        'web3',
        'base58',
        'ecdsa',
        'rlp',
        'eth_utils',
        'two1',
        'pycryptodome'
    ]
)