# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['s4', 's4.clients', 's4.commands']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.7,<2.0',
 'clint>=0.5.1,<0.6.0',
 'filelock>=3.0,<4.0',
 'inotify-simple>=1.1,<2.0',
 'pathspec>=0.5.6,<0.6.0',
 'python-magic>=0.4.15,<0.5.0',
 'tabulate>=0.8.2,<0.9.0',
 'tqdm>=4.23,<5.0']

entry_points = \
{'console_scripts': ['s4 = s4.cli:entry_point']}

setup_kwargs = {
    'name': 's4',
    'version': '0.2.19',
    'description': 'Fast and cheap synchronisation of files using Amazon S3',
    'long_description': None,
    'author': 'Michael Aquilina',
    'author_email': 'michaelaquilina@gmail.com',
    'url': 'https://github.com/MichaelAquilina/S4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
