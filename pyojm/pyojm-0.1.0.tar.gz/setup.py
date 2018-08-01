import sys
from setuptools import setup, find_packages
sys.path.append('./pyojm')
sys.path.append('./tests')

install_requires = [
    'jsonpath_rw',
    'typeguard'
]

setup(
    name='pyojm',
    version="0.1.0",
    author='lune*',
    author_email='lune@wuvu.net',
    description='A Pythonic Interface to Json.',
    license='MIT',
    keywords='json wrapper model',
    install_requires=install_requires,
    url='https://github.com/lune_sta/json-model',
    packages=find_packages(exclude='tests'),
    test_suite='tests'
)

