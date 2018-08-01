from setuptools import setup, find_packages
from os import path
import setuptools

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "pyg3D",
    version = "1.0.1",
    description = "A simple 3D rendering library for python",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url = "https://gitlab.com/ll13s5h/pyg3D",
    author = "Sam H",
    author_email = "ll13s5h@leeds.ac.uk",
    packages = setuptools.find_packages(),
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',


        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    keywords = 'simple 3D games graphics',
    install_requires = ["pyglet","numpy", "PyOpenGL"],
    python_requires='>=3',

)
