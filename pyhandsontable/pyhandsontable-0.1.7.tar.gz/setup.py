# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyhandsontable']

package_data = \
{'': ['*'], 'pyhandsontable': ['templates/*']}

install_requires = \
['jinja2>=2.10,<3.0', 'jupyter>=1.0,<2.0', 'notebook>=5.6,<6.0']

setup_kwargs = {
    'name': 'pyhandsontable',
    'version': '0.1.7',
    'description': 'Bring the power of Handsontable to Python and Jupyter Notebook',
    'long_description': '# pyhandsontable\n\n[![Build Status](https://travis-ci.org/patarapolw/pyhandsontable.svg?branch=master)](https://travis-ci.org/patarapolw/pyhandsontable)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n[![PyPI license](https://img.shields.io/pypi/l/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n\nView a 2-D array, probably from [pyexcel](https://github.com/pyexcel/pyexcel) in Jupyter Notebook, and export to `*.html`.\n\n## Installation\n\n```commandline\npip install pyhandsontable\n```\n\n## Usage\n\n```python\n>>> from pyhandsontable import generate_html, view_table\n>>> view_table(width=800, height=500, data=data_matrix, **kwargs)\n```\n\n## Acceptable kwargs\n\n- title: title of the HTML file\n- maxColWidth: maximum column width. Set to 200.\n- css: url of the Handsontable CSS\n- js: url of the Handsontable Javascript\n- css_custom: your custom CSS\n- js_pre: Javascript before rendering the table (but after most other things.)\n- js_post: Javascript after rendering the table.\n- config: add additional config as defined in https://docs.handsontable.com/pro/5.0.0/tutorial-introduction.html\n  - This will override the default config (per key basis) which are:\n  \n```javascript\n{\n  rowHeaders: true,\n  colHeaders: true,\n  dropdownMenu: true,\n  filters: true,\n  modifyColWidth: function(width, col){\n    if(width > maxColWidth) return maxColWidth;\n  }\n}\n```\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pyhandsontable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
