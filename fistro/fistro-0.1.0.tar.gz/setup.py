# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fistro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fistro',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
