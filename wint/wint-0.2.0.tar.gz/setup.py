# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wint', 'wint.punq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wint',
    'version': '0.2.0',
    'description': 'Dependency injection with type hints',
    'long_description': 'Wint - dependency injection with type hints.\n============================================\n\n[![Build Status](https://travis-ci.org/asyncee/wint.svg?branch=master)](https://travis-ci.org/asyncee/wint)\n[![Coverage Status](https://coveralls.io/repos/github/asyncee/wint/badge.svg?branch=master)](https://coveralls.io/github/asyncee/wint?branch=master)\n\nIntro\n-----\n\nWint is a lightweight library that implements dependency injection via type hinting.\n\nInstallation\n------------\n\nJust use pip:\n```\n$ pip install wint\n```\n\nHow it works\n------------\n\nThere are a ton of approaches to DI, and this library implements only property injection.\n\nWhen ``autowired`` decorator is applied then class is inspected for all\nannotated properties. If property has no value, then it is replaced with ``DependencyDescriptor``.\n\nDependency is resolved when attribute is accessed on instantiated class instance.\n\nThis behaviour allows to resolve dependencies in lazy manner with the downside of a side effect — instance\nreceives a descriptor property that was not existed earlier.\n\nExample\n-------\n\n```python\nfrom wint import autowired, ContainerProvider\n\n\nclass Printer:\n    """Abstract class for printing messages."""\n\n    def print(self, message):\n        raise NotImplementedError\n\n\nclass RealPrinter(Printer):\n    """Implementation of `Printer` which uses `print` to output messages."""\n\n    def print(self, message):\n        print(message)\n\n\n@autowired()\nclass PrintService:\n    # RealPrinter will be automatically injected on property access.\n    printer: Printer\n\n    def run(self, msg):\n        self.printer.print(f"{msg}, i\'m running!")\n\n\nif __name__ == "__main__":\n    container = ContainerProvider.get()\n    # Register RealPrinter as singleton implementation of Printer.\n    container.register(Printer, RealPrinter())\n\n    PrintService().run(\'hey\')\n```\n\n```bash\n$ python example.py\nhey, i\'m running!\n```\n\nNotes\n-----\nThis library is built on [punq](https://github.com/bobthemighty/punq)\n(MIT License) and uses it\'s vendored version.\n',
    'author': 'Stanislav Lobanov',
    'author_email': 'n10101010@gmail.com',
    'url': 'https://github.com/asyncee/wint',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
