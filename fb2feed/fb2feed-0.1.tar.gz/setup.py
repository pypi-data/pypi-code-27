from setuptools import setup
import os

from fb2feed import __version__

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read('README.md')
requirements = map(str.strip, open('requirements.txt').readlines())

setup(
    name='fb2feed',
    version=__version__,
    description="Transforms Facebook pages to Atom feeds",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
        "Topic :: Utilities",
        'License :: OSI Approved :: MIT License'
    ],
    keywords='facebook feed atom',
    author='Philippe Normand',
    author_email='phil@base-art.net',
    url='https://gitlab.com/philn/fb2feed',
    license='MIT License',
    zip_safe=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'fb2feed = fb2feed:main'
        ]
    },
    py_modules = ['fb2feed',],
 )
