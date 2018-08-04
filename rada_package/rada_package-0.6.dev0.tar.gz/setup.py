from setuptools import setup, find_packages
import sys, os

version = '0.6'

setup(name='rada_package',
      version=version,
      description="Rada with abstract factory",
      long_description="""\
Ukraine and Poland radas with abstract factory""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='abstract factory python itea',
      author='Taras Vaskiv',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
            'console_scripts': [
                  'rada = rada_package.verh_rada:main',
            ]
      },
      )
