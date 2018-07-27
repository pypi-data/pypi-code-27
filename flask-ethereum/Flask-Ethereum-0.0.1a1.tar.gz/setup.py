"""
Flask-Ethereum
--------------

Rapid GUI Development for Ethereum Smart Contracts in Flask
"""

from setuptools import setup


setup(
    name='Flask-Ethereum',
    version='0.0.1a1',
    url='https://github.com/fubuloubu/flask-ethereum',
    license='MIT',
    author='Bryant Eisenbach',
    author_email='bryant@dappdevs.org',
    description='Rapid GUI Development for Ethereum Smart Contracts in Flask',
    long_description=__doc__,
    packages=['flask_ethereum'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask',
        'eth-tester[py-evm]',
        'web3'
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
