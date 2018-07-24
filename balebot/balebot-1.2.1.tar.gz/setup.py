import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()
setuptools.setup(name='balebot',
                 version='1.2.1',
                 description='python framework for Bale messenger Bot API ',
                 author='bale',
                 author_email='balebot@elenoon.ir',
                 license='GNU',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 install_requires=[
                     'aiohttp==2.3.7',
                     'asyncio==3.4.3',
                     'graypy==0.2.14',
                 ],
                 packages=setuptools.find_packages())
