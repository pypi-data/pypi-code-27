# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sansio_lsp_client']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.1,<19.0', 'cattrs>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'sansio-lsp-client',
    'version': '0.1.0',
    'description': 'An implementation of the client side of the LSP protocol, useful for mbedding easily in your editor.',
    'long_description': None,
    'author': 'Purple Myst',
    'author_email': 'PurpleMyst@users.noreply.github.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
