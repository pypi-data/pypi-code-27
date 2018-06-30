# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


MODULE_NAME = "DataProperty"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
MISC_DIR = "misc"
REQUIREMENT_DIR = "requirements"

pkg_info = {}


def need_pytest():
    return set(["pytest", "test", "ptr"]).intersection(sys.argv)


def get_release_command_class():
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME.lower(), "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding="utf8") as f:
    long_description = f.read()

with io.open(os.path.join(MISC_DIR, "summary.txt"), encoding="utf8") as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

pytest_runner_require = ["pytest-runner"] if need_pytest() else []
setuptools_require = ["setuptools>=38.3.0"]

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=["data", "property"],
    license=pkg_info["__license__"],
    long_description=long_description,
    maintainer=pkg_info["__author__"],
    maintainer_email=pkg_info["__email__"],
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Tracker": "{:s}/issues".format(REPOSITORY_URL),
    },

    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require + pytest_runner_require,
    tests_require=tests_requires,
    extras_require={
        "build": "wheel",
        "docs": docs_requires,
        "release": "releasecmd>=0.0.10",
        "test": tests_requires,
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass=get_release_command_class())
