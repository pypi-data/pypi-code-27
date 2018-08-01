# coding: utf-8

"""
    Wavefront Dispatch Wrapper

    <p>This is a Wavefront python wrapper for dispatch python function handler to send metrics directly to wavefront.</p>  # noqa: E501
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "wavefront_dispatch"
VERSION = "0.0.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["wavefront-pyformance >= 0.9.2"]

setup(
    name=NAME,
    version=VERSION,
    description="Wavefront Python Wrapper for Dispatch",
    author_email="",
    url="https://github.com/dispatchframework/wavefront-dispatch-python/tree/master",
    keywords=["Wavefront Dispatch", "Wavefront"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    long_description="""\
    This is a Wavefront python wrapper for Dispatch function handler to send metrics directly to wavefront.
    """
)
