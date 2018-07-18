# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ignorio']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0', 'colorama>=0.3.9,<0.4.0', 'requests>=2.19,<3.0']

entry_points = \
{'console_scripts': ['ig = ignorio.cli:main']}

setup_kwargs = {
    'name': 'ignorio',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Franccesco Orozco',
    'author_email': 'franccesco.orozco@codingdose.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
