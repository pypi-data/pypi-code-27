# -*- coding: utf-8 -*-
"""Installer for the plone.oidc package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
        'plone.restapi>=3.2.1'
        'plone.schema>=1.2.0',
        'plone.api>=1.8.4',
        'Products.GenericSetup>=1.8.2',
        'oic',
        'pysaml2',
        'certifi',
        'setuptools',
        'z3c.jbot',

]

membrane_requires = [
    'dexterity.membrane>=2.0.1',
    'Products.membrane>=4.0.0',
]

test_requires = [
    'plone.app.testing',
    # Plone KGS does not use this version, because it would break
    # Remove if your package shall be part of coredev.
    # plone_coredev tests as of 2016-04-01.
    'plone.testing>=5.0.0',
    'plone.app.contenttypes',
    'plone.app.robotframework[debug]',
]

setup(
    name='plone.oidc',
    version='1.0.0a2',
    description="OpenID Connect implementation in Plone",
    long_description=long_description,
    # Get more from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone OpenID oAuth2',
    author='Md Nazrul Islam',
    author_email='email2nazrul@gmail.com',
    url='https://pypi.org/project/plone.oidc',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['plone'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires + membrane_requires,
        'membrane': membrane_requires
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
