#!/usr/bin/env python

from setuptools import setup


long_description = """
A tool to automate build steps from README files.
"""

setup(name="buildok",
    packages=[
        "buildok",
        "buildok.readers",
        "buildok.statements",
        "buildok.structures",
        "buildok.util",
        "buildok.converters",
    ],
    entry_points = {
        "console_scripts": [
            "build = buildok.bootstrap:main"
        ]
    },
    version="0.4.0",
    description="A tool to automate build steps from README files.",
    long_description=long_description,
    author="Alexandru Catrina",
    author_email="alex@codeissues.net",
    license="MIT",
    url="https://github.com/lexndru/buildok",
    download_url="https://github.com/lexndru/buildok/archive/v0.4.0.tar.gz",
    keywords=["build-tool", "build-automation", "readme", "buildok"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
)
