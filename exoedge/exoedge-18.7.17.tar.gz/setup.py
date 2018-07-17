"""
Installer for ExoSense Client
"""
import os
from setuptools import setup, find_packages
from exoedge import __version__

DOCS_URL = 'https://github.com/exosite/lib_exoedge_python'


def read(fname):
    """ Primarily used to open README file. """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

try:
    README = read('README.rst')
except:
    README = ''

setup(
    name="exoedge",
    version=__version__,
    author="Exosite LLC",
    author_email="support@exosite.com",
    description="""The ExoSense Client is the Python library for interacting with Exosite's ExoSense Industrial IoT Solution.""",
    license="Apache 2.0",
    keywords="murano exosite iot iiot gateway edge exoedge exosense",
    url="https://github.com/exosite/lib_exoedge_python",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'edged = exoedge.edged:main'
        ]
    },
    install_requires=['docopt>=0.6.2', 'murano-client>=18.7.1'],
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: Apache Software License",
    ],
    data_files=[])
