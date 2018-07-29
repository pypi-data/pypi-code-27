# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'foliant'}

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['foliant>=1.0,<2.0', 'semver>=2.8,<3.0']

setup_kwargs = {
    'name': 'foliantcontrib.bump',
    'version': '1.0.0',
    'description': 'Version bumper for Foliant projects.',
    'long_description': None,
    'author': 'Konstantin Molchanov',
    'author_email': 'moigagoo@live.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
