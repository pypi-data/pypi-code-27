""" Installer for Murano Client protocol layer. """
# pylint: disable=I0011,W0312,C0410
import os
from murano_client.__version__ import __version__
from setuptools import setup, find_packages

DOCS_URL = 'github.com/exosite/lib_murano_client_python'

REQUIREMENTS = [
    'docopt>=0.6.2',
    'requests>=2.13.0',
    'paho-mqtt',
    'six'
]

def read(fname):
    """ Primarily used to open README file. """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

try:
    README = read('README.rst')
except:
    README = ''

setup(
    name="murano_client",
    version=__version__,
    author="Exosite LLC",
    author_email="support@exosite.com",
    description="""Murano Device Client is the primary library for communicating with the Exosite Murano Platform.""",
    license="Apache 2.0",
    keywords="murano exosite iot iiot client gateway",
    url="https://github.com/exosite/lib_murano_client_python",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gdc = murano_client.gdc:main',
        ]
    },
    install_requires=REQUIREMENTS,
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: Apache Software License",
    ],
    include_package_data=True,
)
