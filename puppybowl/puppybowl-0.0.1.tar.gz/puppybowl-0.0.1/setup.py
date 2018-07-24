from setuptools import setup, find_packages

setup (
  name = 'puppybowl',
  version = '0.0.1',
  url = 'https://github.com/GiovanniCardamone/PuppyBowl',
  description = 'Puppy Bowl Server',
  author = 'Giovanni Cardamone',
  author_email = 'g.cardamone2@gmail.com',
  license = 'MIT',
  packages = find_packages(exclude=['contrib', 'docs', 'tests']),
  install_requires = [],
  python_requires = '>=3',
  entry_points = {
    'console_scripts': [
      'puppybowl = app.main:main'
    ]
  }
)