#from distutils.core import setup
from setuptools import setup

version='0.1.5'

setup(
    name='oreumums',
    version=version,
    packages=['oreumums'],
    author='alghost',
    author_email='alghost@moreum.co.kr',
    url='https://api.smsrang.co.kr',
    description='A package for using UMS service of Oreum Corporation.',
    install_requires=[
        'requests'
    ]
)
