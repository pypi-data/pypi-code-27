#setup file from mpesa wrapper

from setuptools import setup

setup(name='python_mpesawrapper',
      version='1.0.4',
      description='python wrapper for the new mpesa daraja api',
      url='https://gitlab.com/Quantumke/mpesawrapper',
      author='Benson Nguru',
      author_email='nguruben@gmail.com',
      license='MIT',
      packages=['python_mpesawrapper'],
      install_requires=[
            'nose',
            'requests',
            'sphinx_rtd_theme'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )