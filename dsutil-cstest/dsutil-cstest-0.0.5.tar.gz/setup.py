# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsutil-cstest",
    version="0.0.5",
    author="zgyy",
    author_email="cs25216@163.com",
    description="Collection of utils for making your life easier when using the Python data science stack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'matplotlib>=2.0.0',
        'pandas>=0.20.0'
    ],
    url="https://github.com/caisong25216/zgyytest",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",	
    ),
)
