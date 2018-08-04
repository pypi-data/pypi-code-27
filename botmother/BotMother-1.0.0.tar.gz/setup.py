#!/usr/bin/env python
"""The setup and build script for the python-telegram-bot library."""

from setuptools import setup, find_packages


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = find_packages()

setup(name='BotMother',
    version="1.0.0",
    author='Insight Data Science Lab',
    author_email='insightlab@dc.ufc.br',
    license='MIT',
    url='',
    keywords='python telegram bot api wrapper bot mother botmother',
    description="A new perspective over python-telegram-bot API",
    long_description=long_description,
    packages=packages,
    install_requires=requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],)