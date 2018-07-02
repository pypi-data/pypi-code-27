#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['idataapi_transform',
 'idataapi_transform.DataProcess',
 'idataapi_transform.DataProcess.Config',
 'idataapi_transform.DataProcess.Config.ConfigUtil',
 'idataapi_transform.DataProcess.DataGetter',
 'idataapi_transform.DataProcess.DataWriter',
 'idataapi_transform.DataProcess.Meta']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'openpyxl', 'elasticsearch-async']

entry_points = \
{'console_scripts': ['transform = idataapi_transform:main']}

setup(name='idataapi-transform',
      version='1.2.0',
      description='convert data from a format to another format, read or write from file or database, suitable for iDataAPI',
      author='zpoint',
      author_email='zp@zp0int.com',
      url='https://github.com/zpoint/idataapi-transform',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.5.2',
     )
