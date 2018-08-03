from setuptools import setup, find_packages
from pyvat import __VERSION__

setup(
    name="ZITPyVAT",
    version=__VERSION__,
    packages=find_packages(),
    description='ZIT python vat common packages',
    long_description=open('README.rst').read(),
    url='http://www.tjzit.com/',
    license='None',
    author='olxjdq',
    author_email='liugang@gosusncn.com',
    maintainer='Linsen',
    maintainer_email='linsen@gosuncn.com',
    py_modules=[
        'pyvat.py_sa_opr',
        'pyvat.ratb5',
        'pyvat.SignalGenerator',
        'pyvat.Socket_Func',
        'pyvat.vatbase'
    ],
    install_requires=['PyVISA>=1.8'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7'
    ],
)
