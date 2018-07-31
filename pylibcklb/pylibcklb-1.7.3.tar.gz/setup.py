## Setup file for the pylibcklb package
#
# @file		    setup.py
# @author	    Tobias Ecklebe
# @date		    02.11.2017
# @version	    0.1.0
# @bug          No bugs at the moment.
#
# @copyright    pylibcklb package
#               Copyright (C) 2017  Tobias Ecklebe
#
#               This program is free software: you can redistribute it and/or modify
#               it under the terms of the GNU Lesser General Public License as published by
#               the Free Software Foundation, either version 3 of the License, or
#               (at your option) any later version.
#
#               This program is distributed in the hope that it will be useful,
#               but WITHOUT ANY WARRANTY; without even the implied warranty of
#               MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#               GNU Lesser General Public License for more details.
#
#               You should have received a copy of the GNU Lesser General Public License
#               along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# imports
import os
from setuptools import setup, find_packages
from pylibcklb.metadata import Variables

def readme():
    try:
        import pypandoc
        rst = pypandoc.convert_file('README.md', 'rst')
        rst = rst.replace("\r","")
        return rst
    except (OSError, ImportError):
        print('If pandoc is not installed, just return the raw markdown text')
        with open('README.md') as f:
            return f.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG'][1:]
else:
    version = os.environ['CI_JOB_ID']

setup(name=Variables.name,
      version=version,
      description=Variables.description,
      long_description=readme(),
      classifiers=Variables.classifiers,
      url=Variables.url,
      download_url=Variables.download_url,
      author=Variables.author,
      author_email=Variables.author_email,
      license=Variables.license,
      packages=find_packages(),
      python_requires='>=3',
      setup_requires=Variables.install_requires,
      install_requires=Variables.install_requires,
      extras_require=Variables.extras_require,
      test_suite='nose.collector',
      tests_require=Variables.test_require,
      #scripts=find_scripts(),
      include_package_data=True,
      zip_safe=False)
