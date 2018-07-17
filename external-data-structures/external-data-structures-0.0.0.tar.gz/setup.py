import os
from setuptools import setup, find_packages

dir_path = os.path.dirname(os.path.realpath(__file__))

VERSION = open(os.path.join(dir_path, 'VERSION')).read()

setup(
  name = 'external-data-structures',
  packages = find_packages(),
  version = VERSION,
  description = '''
  A set of data structure abstractions for various external data stores.
  ''',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Marco Montagna',
  author_email = 'marcojoemontagna@gmail.com',
  url = 'https://github.com/mmontagna/extra-dict',
  keywords = ['dictionary', 'dicts', 's3', 'redis', 'sets'],
  classifiers=(
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
  ),
  data_files = [('', ['LICENSE', 'VERSION'])],
  include_package_data=True,
  python_requires=">=2.7",
  license=open(os.path.join(dir_path, 'LICENSE')).read(),
  install_requires=[
    "generic-encoders>=0.3.2",
    "recursive-itertools>=0.1.0"
  ],

  extras_require={
      's3':  ["boto3>=1.7.40"],
      'dev': [
        'moto'
      ]
  },
  entry_points = {
  },
)