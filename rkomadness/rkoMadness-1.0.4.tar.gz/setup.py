#setup file from mpesa wrapper

from setuptools import setup

setup(name='rkoMadness',
      version='1.0.4',
      description='python package for rkoMadness',
      url='https://gitlab.com/Quantumke/rkoMadness',
      author='Benson Nguru',
      author_email='nguruben@gmail.com',
      license='MIT',
      packages=['rkoMadness'],
      install_requires=[
            'nose',
            'requests',
            'sphinx_rtd_theme',
            'termcolor'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/rkomadness:strartproject'],
      )