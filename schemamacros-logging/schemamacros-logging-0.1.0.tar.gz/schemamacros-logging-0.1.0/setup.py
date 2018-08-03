"""
Logging for schemamacros
----------------

Logging package for schemamacros.

look at schemamacros for more info

"""

from setuptools import setup, find_packages


setup(
    name='schemamacros-logging',
    version='0.1.0',
    url='https://github.com/caj-larsson/schemamacros-logging',
    license='MIT',
    author='Caj Larsson',
    author_email='contact@caj.me',
    description='logging for schemamacros',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'schemamacros',
    ],
    package_dir={'schemamacros-logging': 'schemamacros-logging'},
    package_data={'schemamacros-loggng': ['templates/*.sql']},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
