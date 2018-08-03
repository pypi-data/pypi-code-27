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
    'version': '0.1.4',
    'description': 'Excel workbook with no formula conversion, but with markdown/HTML support.',
    'long_description': '# Simplecel\n\n[![Build Status](https://travis-ci.org/patarapolw/simplecel.svg?branch=master)](https://travis-ci.org/patarapolw/simplecel)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n[![PyPI license](https://img.shields.io/pypi/l/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n\nExcel workbook with no formula conversion, but with markdown/HTML support.\n\n## Installation\n\n```commandline\npip install simplecel\npip install pyexcel-xls  # Or any other packages defined in pyexcel GitHub\n```\n\nFor what you need to install other than `simplecel`, please see https://github.com/pyexcel/pyexcel#available-plugins\n\n## Usage\n\n```commandline\n$ simplecel --help\nUsage: simplecel [OPTIONS] FILENAME\n\nOptions:\n  --meta TEXT     Please input the path to META json, as defined in pyexcel-\n                  export.\n  --host TEXT\n  --port INTEGER\n  --debug\n  --help          Show this message and exit.\n$ simplecel example.xlsx\n```\n\n## Plan\n\n- Add API for saving and editing data (should be easy-to-implement).\n- Wrap this app in PyQt / PyFlaDesk for GUI end-users (maybe later, as PyFlaDesk of now is still buggy).\n\n## Screenshots\n\n<img src="https://raw.githubusercontent.com/patarapolw/simplecel/master/screenshots/0.png" />\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/simplecel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
