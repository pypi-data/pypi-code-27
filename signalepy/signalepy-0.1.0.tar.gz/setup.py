# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['signalepy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'signalepy',
    'version': '0.1.0',
    'description': 'Elegant Console Logger For Python Command Line Apps',
    'long_description': '\n# Signale.py\nAn Elegant Python Console Logger',
    'author': 'Shardul Nalegave',
    'author_email': 'nalegaveshardul40@gmail.com',
    'url': 'https://github.com/ShardulNalegave/signale.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
