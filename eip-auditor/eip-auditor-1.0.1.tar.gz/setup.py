#!/usr/bin/env python
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/SpekoTechnologies/eip-auditor
"""

# Always prefer setuptools over distutils
from io import open
from setuptools import setup, find_packages

setup(
    name='eip-auditor',  # Required
    version='1.0.1',  # Required
    url='https://github.com/SpekoTechnologies/eip-auditor',  # Optional
    author='Speko Technologies',  # Optional
    author_email='info@speko.io',  # Optional
    description='An AWS EIP Auditor',  # Required
    packages=find_packages(),  # Required
    long_description=open('README.md').read(),  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        "argparse",
        "boto3",
        "emojipedia",
        "bs4",
        "requests"
    ],
    entry_points={  # Optional
        'console_scripts': [
            'eip-auditor=eip_auditor.cmdline:execute',
        ],
    },
    keywords='eip auditor aws vpc elastic ip addresses',  # Optional
)
