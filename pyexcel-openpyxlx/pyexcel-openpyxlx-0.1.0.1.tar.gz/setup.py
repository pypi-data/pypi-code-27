# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyexcel_openpyxlx']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=2.5,<3.0', 'ruamel.yaml>=0.15.50,<0.16.0']

setup_kwargs = {
    'name': 'pyexcel-openpyxlx',
    'version': '0.1.0.1',
    'description': 'Export styles from Excel using OpenPyXL (for XlsxWriter -- pyexcel-xlsxwx)',
    'long_description': None,
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pyexcel-openpyxlx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
