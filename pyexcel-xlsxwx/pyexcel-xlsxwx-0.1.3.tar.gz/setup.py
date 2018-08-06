# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyexcel_xlsxwx']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0',
 'ruamel.yaml>=0.15.50,<0.16.0',
 'xlsxwriter>=1.0,<2.0']

setup_kwargs = {
    'name': 'pyexcel-xlsxwx',
    'version': '0.1.3',
    'description': 'Save pyexcel data with XlsxWriter, while retaining good formatting.',
    'long_description': '# pyexcel-xlsxwx\n\n[![Build Status](https://travis-ci.org/patarapolw/pyexcel-xlsxwx.svg?branch=master)](https://travis-ci.org/patarapolw/pyexcel-xlsxwx)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pyexcel_xlsxwx.svg)](https://pypi.python.org/pypi/pyexcel_xlsxwx/)\n[![PyPI license](https://img.shields.io/pypi/l/pyexcel_xlsxwx.svg)](https://pypi.python.org/pypi/pyexcel_xlsxwx/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyexcel_xlsxwx.svg)](https://pypi.python.org/pypi/pyexcel_xlsxwx/)\n\nSave pyexcel data with XlsxWriter, while retaining good formatting.\n\n## Features\n\n- Allow setting column widths and word wrap.\n- A package for reading data is not included, please see [`pyexcel`\'s plugins here](https://github.com/pyexcel/pyexcel#available-plugins).\n\n## Installation\n\n```commandline\n$ pip install pyexcel-xlsxwx\n```\nNote that `pyexcel` is not a dependency.\n\n## Usage\n\n```python\n>>> import pyexcel_xlsxwx\n>>> data = OrderedDict() # from collections import OrderedDict\n>>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})\n>>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})\n>>> pyexcel_xlsxwx.save_data("your_file.xlsx", data)\n```\n\nYou can also define a custom config via:\n```python\n>>> pyexcel_xlsxwx.save_data("your_file.xlsx", data, config=config)\n```\nWhere config can be dictionary or path to YAML file.\n\nThe default YAML config is:\n\n```yaml\nworkbook:\n  constant_memory: true\n  strings_to_numbers: false\n  strings_to_formulas: false\n  strings_to_urls: true\nworksheet:\n  _default:\n    freeze_panes: A2\n#    column_width: 30\n    smart_fit: true\n    max_column_width: 30\nformat:\n  _default:\n    valign: top\n    text_wrap: true\n```\n`column_width` can also accept a list of numbers.\n\nFor example, to cancel out `freeze_panes`, try:\n\n```python\n>>> pyexcel_xlsxwx.save_data("your_file.xlsx", data, config={\'worksheet\': {\'_default\': {\'freeze_panes\': None}}})\n```\n\nThe settings will merge (thanks to https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data), so that the other formattings won\'t be lost.\n\n## Associated projects\n\n- [pyexcel-export](https://github.com/patarapolw/pyexcel-export) - operates using OpenPyXL, which seeming has bad word wrap support. However, the formatting can be well preserved.\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pyexcel-xlsxwx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
