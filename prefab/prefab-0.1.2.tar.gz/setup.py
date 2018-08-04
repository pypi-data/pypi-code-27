import codecs
import os.path

from setuptools import setup


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


setup(
    name='prefab',
    version='0.1.2',
    description='Prefabricate a python project!',
    long_description=read(fpath('README.rst')),
    url='http://github.com/zackhsi/prefab',
    author='Zack Hsi',
    author_email='zackhsi@gmail.com',
    license='MIT',
    packages=['prefab'],
    entry_points={
        'console_scripts': [
            'prefab = prefab.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
