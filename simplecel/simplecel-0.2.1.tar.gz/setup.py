# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simplecel']

package_data = \
{'': ['*'], 'simplecel': ['static/*', 'static/vendor/*', 'templates/*']}

install_requires = \
['click>=6.7,<7.0',
 'flask>=1.0,<2.0',
 'pyexcel>=0.5.8,<0.6.0',
 'ruamel.yaml>=0.15.48,<0.16.0']

entry_points = \
{'console_scripts': ['simplecel = simplecel.__main__:load_excel']}

setup_kwargs = {
    'name': 'simplecel',
    'version': '0.2.1',
    'description': 'Offline Excel-like app with no formula conversion, but with image/markdown/HTML support.',
    'long_description': '# Simplecel\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n[![PyPI license](https://img.shields.io/pypi/l/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/simplecel.svg)](https://pypi.python.org/pypi/simplecel/)\n\nOffline Excel-like app with no formula conversion, but with image/markdown/HTML support.\n\n## Features\n\n- Custom renderers beyond https://docs.handsontable.com/5.0.0/demo-custom-renderers.html -- \'markdownRenderer\', \'imageRenderer\'. -- Can render images with URL\'s alone. No need for `<img src="" />`.\n- Always good word wrap support and auto-row-height due to Handsontable.\n- Absolutely no formula conversion. Things like `=1+2`, `OCT2`, `11-14` will never get converted.\n- Max column width can be specified (default: 200).\n\n## Installation\n\n```commandline\npip install simplecel\npip install pyexcel-xlsx  # Or any other packages defined in pyexcel GitHub\n```\n\nFor what you need to install other than `simplecel`, please see https://github.com/pyexcel/pyexcel#available-plugins\n\n## Usage\n\n```commandline\n$ simplecel --help\nUsage: simplecel [OPTIONS] FILENAME\n\nOptions:\n  --config TEXT     Please input the path to CONFIG json, as defined in pyhandsontable.\n  --host TEXT\n  --port INTEGER\n  --debug\n  --help          Show this message and exit.\n$ simplecel example.xlsx\n```\n\nIn this case, `example.config.json` is also auto-loaded, although you can specify `*.config.json` directly in `--config`. If the file doesn\'t exist, it will be auto-generated on Save.\n\n## Example of `example.config.json`\n\n```json\n{\n  "hanzi": {\n    "hasHeader": true,\n    "renderers": "markdownRenderer"\n  },\n  "vocab": {\n    "hasHeader": true,\n    "renderers": "markdownRenderer"\n  },\n  "sentences": {\n    "hasHeader": true,\n    "renderers": "markdownRenderer"\n  }\n}\n```\n\nNote that the `defaultConfig` are\n\n```javascript\n{\n  rowHeaders: true,\n  colHeaders: true,\n  manualRowResize: true,\n  manualColumnResize: true,\n  filters: true,\n  dropdownMenu: true,\n  contextMenu: true,\n  maxColWidth: 200,\n  hasHeader: false\n}\n```\n\n`renderers` can also accept something like\n\n```python\n{\n    1: "markdownRenderer",\n    2: "markdownRenderer"\n}\n```\n\nSome other acceptable configs are defined in https://docs.handsontable.com/5.0.0/Options.html\n\n## Plan\n\n- Wrap this app in PyQt / PyFlaDesk for GUI end-users (maybe later, as PyFlaDesk of now is still buggy).\n\n## Screenshots\n\n<img src="https://raw.githubusercontent.com/patarapolw/simplecel/master/screenshots/0.png" />\n',
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
