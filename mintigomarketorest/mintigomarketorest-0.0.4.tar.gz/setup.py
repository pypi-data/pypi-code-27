import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pymarketo'))

# python setup.py register -r pypi
# python setup.py sdist upload -r pypi

long_description = '''
Mintigo Marketo Python REST is a Python client that wraps the Marketo Rest API.
Originally developed by Eliram based on a package by asamat with contributions from sandipsinha
'''

setup(
    name='mintigomarketorest',
    version= '0.0.4',
    url='https://bitbucket.org/mintigo/marketo-rest-python',
    author='Eliram Shatz',
    author_email='eliram@mintigo.com',
    packages=['mintigomarketorest', 'mintigomarketorest.helper'],
    license='MIT License',
    install_requires=[
        'requests==2.10.0',
    ],
    keywords = ['Marketo', 'Mintigo', 'REST API', 'Wrapper', 'Client'],
    description='Python Client for Mintigo for the Marketo REST API',
    long_description=long_description
)
