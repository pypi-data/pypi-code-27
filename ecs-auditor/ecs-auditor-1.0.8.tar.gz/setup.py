#!/usr/bin/env python
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/SpekoTechnologies/ecs-auditor
"""

# Always prefer setuptools over distutils
from io import open
from setuptools import setup, find_packages

setup(
    name='ecs-auditor',  # Required
    version='1.0.8',  # Required
    url='https://github.com/SpekoTechnologies/ecs-auditor',  # Optional
    author='Speko Technologies',  # Optional
    author_email='info@speko.io',  # Optional
    description='An ECS Auditor',  # Required
    packages=find_packages(),  # Required
    long_description=open('README.rst').read(),  # Optional
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
    setup_requires=[
        "ansible",
    ],
    install_requires=[
        "boto3==1.7.41",
        "jsondiff",
        "PyGithub==1.40",
        "python-coveralls==2.7.0",
        "python-dateutil==2.7.3",
        "python-jose-ext==1.3.2.2",
        "simplejson",
        "pyaml==17.10.0",
        "ansible-vault",
        "xlsxwriter",
    ],
    entry_points={  # Optional
        'console_scripts': [
            'ecs-auditor=ecs_auditor.cmdline:execute',
        ],
    },
    keywords='ecs auditor aws ssm python',  # Optional
)
