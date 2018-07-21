# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="affine6p-cstest",
    version="0.8.1",
    description="To calculate affine transformation parameters with six free parameters.",
    long_description=long_description,
    url="https://gitlab.com/yoshimoto/affine6p-py",
    author="zgyy",
    author_email="347186678@qq.com",
    license="MIT",
    keywords="calculate affine transformation six parameters",
    packages=["affine6p-cstest"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        ]
)