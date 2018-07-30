#!/usr/bin/env python3
from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name = 'redditcli',
    version = '1.1.0',
    description = 'A command line application that lets you browse Reddit.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = 'Yathartha Goel',
    license = 'MIT License',
    platforms = 'Cross Platform',
    packages = find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = [
        'click',
        'praw',
        'prompt_toolkit == 1.0.15',
        'pygments'
    ],
    entry_points = {
        "console_scripts": ['reddit = reddit.main:cli',
                            'rdt = reddit.main_rdt:cli']
        }
    )
