# -*- coding: utf-8 -*-
# pylint: skip-file
import codecs
import os
import sys
from distutils.core import setup

from setuptools import find_packages

with open('prospector2/__pkginfo__.py') as f:
    exec(f.read())
_VERSION = globals()['__version__']


_PACKAGES = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_INSTALL_REQUIRES = [
    'pylint-plugin-utils>=0.2.6',
    'requirements-detector>=0.6',
    'setoptconf>=0.2.0',
    'dodgy>=0.1.9',
    'pyyaml',
    'mccabe>=0.5.0',
    'pyflakes<2.0.0,>=0.8.1',
    'pycodestyle<2.4.0,>=2.0.0',
    'pep8-naming>=0.3.3',
    'pydocstyle>=2.0.0',
    'pylint<2',
]

_PACKAGE_DATA = {
    'prospector2': [
        'blender_combinations.yaml',
    ]
}
profiledir = os.path.join(os.path.dirname(__file__), 'prospector2/profiles/profiles')
_PACKAGE_DATA['prospector2'] += [profile for profile in os.listdir(profiledir)]

_CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: '
    'GNU General Public License v2 or later (GPLv2+)',
]

_OPTIONAL = {
    'with_frosted': ('frosted>=1.4.1',),
    'with_vulture': ('vulture>=0.6,<0.25',),
    'with_pyroma': ('pyroma>=2.3',),
    'build_tools': ('nose', 'coverage', 'coveralls', 'mock'),
}

with_everything = [req for req_list in _OPTIONAL.values() for req in req_list]
_OPTIONAL['with_everything'] = sorted(with_everything)

if os.path.exists('README.rst'):
    _LONG_DESCRIPTION = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    _LONG_DESCRIPTION = 'Prospector: python static analysis tool. See http://prospector.readthedocs.io'


setup(
    name='prospector2',
    version=_VERSION,
    url='http://prospector.readthedocs.io',
    author='landscape.io',
    author_email='code@landscape.io',
    license='GPLv2',
    zip_safe=False,
    description='Prospector: python static analysis tool',
    long_description=_LONG_DESCRIPTION,
    keywords='pylint pyflakes pep8 mccabe frosted prospector static code analysis',
    classifiers=_CLASSIFIERS,
    package_data=_PACKAGE_DATA,
    include_package_data=True,
    packages=_PACKAGES,
    entry_points={
        'console_scripts': [
            'prospector = prospector2.run:main',
            'prospector2 = prospector2.run:main', # duplicate just to make it more friendly to figure out what to run :-)
        ],
    },
    install_requires=_INSTALL_REQUIRES,
    extras_require=_OPTIONAL,
)
