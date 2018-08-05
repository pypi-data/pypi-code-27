# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['checkstat']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0', 'colorama>=0.3.9,<0.4.0', 'requests>=2.19,<3.0']

entry_points = \
{'console_scripts': ['checkstat = checkstat.cli:main']}

setup_kwargs = {
    'name': 'checkstat',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Franccesco Orozco',
    'author_email': 'franccesco.orozco@codingdose.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
