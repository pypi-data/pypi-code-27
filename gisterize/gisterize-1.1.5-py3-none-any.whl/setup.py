from setuptools import setup, find_packages

setup(
    name='gisterize',
    version='1.1.1',
    description='Gist utility to download data',
    author='Quinton Teas',
    author_email='quinton@schemadesign.com',
    url='https://github.com/schemadesign/gisterize',
    keywords='gist data visualization wrapper endpoint',
    packages=find_packages(exclude=['tests'])
)