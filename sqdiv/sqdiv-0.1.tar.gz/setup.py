import os
from setuptools import setup


def read(fname):
    """
    Utility function to read the README file.

    Used for the long_description.  It's nice, because now 1) we have a top
    level README file and 2) it's easier to type in the README file than to put
    a raw string in below.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
      # mandatory
      name="sqdiv",
      # mandatory
      version="0.1",
      # mandatory     author="Eric J. Ma, Justin Zabilansky, Jon Charest",
      author_email="ericmajinglong@gmail.com",
      description=("A small utility to compute the squarest pair of divisors for an integer."),
      license="MIT",
      keywords="math, geometry, matplotlib",
      url="https://github.com/ericmjl/squarest-divisors",
      packages=['sqdiv'],
      package_data={'': ['README.md', 'LICENSE']},
      install_requires=['numpy', 'hypothesis'],
      long_description=read('README.md'),
      classifiers=["Topic :: Scientific/Engineering :: Visualization"],
      )
