from distutils.core import setup
import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name = 'teshu',
  packages=find_packages(),
  include_package_data=True,
  scripts=['teshu/bin/teshu-admin.py'],
  entry_points={'console_scripts': [
      'teshu-admin = teshu.core.management:execute_from_command_line',
  ]},
  install_requires=[
    'elasticsearch-dsl==6.0.1',
    'flasgger==0.8.0',
    'Flask==0.12.2',
    'Flask-Cors==3.0.3',
    'Flask-JWT==0.3.2',
    'Flask-RESTful==0.3.6',
    'marshmallow==2.15.0',
    'bcrypt==3.1.4',
    'pandas==0.23.0'],
  version = '0.0.2',
  description = 'teshu rest framework',
  author = 'Venkata Sai Katepalli',
  author_email = 'venkata.katepalli@inmar.com',
  url = 'https://github.com/teshu/teshu.git',
  download_url = 'https://github.com/teshu/teshu.git',
  keywords = ['teshu', 'rest', 'rest api'], # arbitrary keywords
  classifiers = [],
)
