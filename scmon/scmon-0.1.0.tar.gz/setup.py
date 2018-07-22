import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


version = '0.1.0'


setup(
    name='scmon',
    version=version,
    author='Kris',
    author_email='31852063+krisfris@users.noreply.github.com',
    description=('Dev tool for restarting apps on code change'),
    license='MIT',
    keywords='',
    url='https://github.com/krisfris/scmon',
    packages=find_packages(exclude=['docs', 'tests']),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    data_files=[('', ['LICENSE', 'README.md'])],
    install_requires=[]
)
