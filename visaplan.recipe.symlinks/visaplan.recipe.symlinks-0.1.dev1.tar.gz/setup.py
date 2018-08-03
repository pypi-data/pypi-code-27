# -*- coding: utf-8 -*- vim: et ts=8 sw=4 sts=4 si tw=79 cc=+1
"""Installer for the visaplan.recipe.symlinks package."""

from setuptools import find_packages
from setuptools import setup

VERSION = (open('VERSION').read().strip()
           + '.dev1'  # in branches only
           )



long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='visaplan.recipe.symlinks',
    # see also --> ./visaplan.recipe.symlinks.egg-info/PKG-INFO: 
    version=VERSION,
    description="Create resource symlinks for Zope instances",
    long_description=long_description,
    # Get more from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Buildout",
        "Framework :: Zope",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        'Intended Audience :: System Administrators',
        "Operating System :: POSIX",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    # keywords='Python Plone',
    author='Tobias Herp',
    author_email='tobias.herp@visaplan.com',
    url='https://pypi.org/project/visaplan.recipe.symlinks',
    license='GPL version 2',
    packages=find_packages('src'),
    namespace_packages=[
        'visaplan',
        'visaplan.recipe',
        ],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [zc.buildout]
    default = visaplan.recipe.symlinks:Recipe
    """,
)
