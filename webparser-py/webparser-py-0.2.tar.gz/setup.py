import os

from setuptools import setup
from webparser import __version__

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    # Meta data
    name='webparser-py',
    version=__version__,
    author='Muhammad Azhar',
    author_email='azhar@contentstudio.io',
    maintainer='Muhammad Azhar',
    maintainer_email='azhar@contentstudio.io',
    url='https://contentstudio.io',
    description='A web parser wrapper on top of lxml and selectolax',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    license='MIT License',
    # Package files
    packages=[
        'webparser',
    ],
    include_package_data=True,
    # Dependencies
    install_requires=[
        "lxml", "feedparser", "requests",
    ],
    extras_require={
        'full': ['urllib3', 'certifi'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)
