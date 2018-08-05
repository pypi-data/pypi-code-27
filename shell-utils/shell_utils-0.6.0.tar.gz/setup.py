# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['shell_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0']

entry_points = \
{'console_scripts': ['notify = shell_utils.notify:notify_command',
                     'shell_utils = shell_utils.cli:cli']}

setup_kwargs = {
    'name': 'shell-utils',
    'version': '0.6.0',
    'description': 'Shell automation tools, like Make on steroids.',
    'long_description': None,
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
