#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os

exec(open('navsy/version.py').read())

github_url = 'https://github.com/fabiocaccamo'
package_name = 'django-navsy'
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.rst')
long_description = ''
try:
    with open(long_description_file_path) as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    version=__version__,
    description='django-navsy is a fast navigation system for lazy devs.',
    long_description=long_description,
    author='Fabio Caccamo',
    author_email='fabio.caccamo@gmail.com',
    url='%s/%s' % (github_url, package_name, ),
    download_url='%s/%s/archive/%s.tar.gz' % (github_url, package_name, __version__, ),
    keywords=['django', 'navigation', 'nav', 'system', 'controller', 'router', 'routes', 'urls', 'pages', 'menu', 'breadcrumbs', 'tree', 'fast'],
    requires=['django(>=1.8)'],
    install_requires=[
        'django-autoslug >= 1.9.3, < 2.0.0',
        'django-modeltranslation >= 0.12.2, < 1.0.0',
        'django-treenode >= 0.11.1, < 1.0.0',
        'python-slugify >= 1.2.4, < 1.3.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools',
    ],
    license='MIT',
    test_suite='runtests.runtests',
)
