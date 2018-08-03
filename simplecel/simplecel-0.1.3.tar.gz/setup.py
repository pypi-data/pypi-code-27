# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simplecel']

package_data = \
{'': ['*'], 'simplecel': ['static/*', 'static/vendor/*', 'templates/*']}

install_requires = \
['click>=6.7,<7.0', 'flask>=1.0,<2.0', 'pyexcel>=0.5.8,<0.6.0']

entry_points = \
{'console_scripts': ['simplecel = simplecel.__main__:load_excel']}

setup_kwargs = {
    'name': 'simplecel',
    'version': '0.1.3',
    'description': 'Excel workbook with no formula conversion, but with markdown/HTML support.',
    'long_description': None,
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
