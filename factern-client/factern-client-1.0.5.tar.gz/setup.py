# coding: utf-8

"""
    Factern API
"""

from setuptools import setup, find_packages  # noqa: H301

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
NAME = "factern-client"
URL = "https://github.com/Factern/factern-client-python"
VERSION = "1.0.5"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Factern API",
    author='factern',
    author_email="support@factern.com",
    url=URL,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    keywords=["Swagger", "Factern API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
