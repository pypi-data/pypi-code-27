# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['signalepy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'signalepy',
    'version': '0.1.3',
    'description': 'Elegant Console Logger For Python Command Line Apps',
    'long_description': '\n<div align="center" id="main">\n\t<h1 align="center">Signale.py</h1>\n\t<p align="center">Elegant Console Logger For Python Command-Line Apps</p>\n\t<br>\n\t<br>\n\t<img src="./imgs/main.png" alt="example" align="center">\n</div>\n\n<hr>\n\n\n\n## Installation\n**Signale.py** can be installed using pip.\n\n````bash\n\n    [sudo] pip install signalepy\n\n````\n\n\n\n## Usage\nPackage consists of a class `Signale`, it is the main constructor class. The object created has all the logger functions in it.\n\n\n### Using Loggers\nEach logger function takes in three arguments:-\n- `text`\n- `prefix` ( Optional )\n- `suffix` ( Optional )\n\nThey all are available in the logger object. To create one do this:-\n````python\n\n    from signalepy import Signale\n\n    logger = Signale()\n\n````\n\nNow you can use the default loggers using this object like:-\n````python\n\n    ...\n\n\tlogger.success("Started Successfully", prefix="Debugger")\n\tlogger.warning("`a` function is deprecated", suffix="main.py")\n\tlogger.complete("Run Complete")\n\n    ...\n\n````\n\n\nThis will produce the following result:-\n\n<div align="center">\n\t<img align="center" src="./imgs/result.png">\n</div>\n\n<br><br>\n\n<details>\n\t<summary>View All Available Loggers</summary>\n\n- `simple`\n- `success`\n- `error`\n- `warning`\n- `start`\n- `stop`\n- `watch`\n- `important`\n- `pending`\n- `complete`\n- `debug`\n- `pause`\n- `info`\n- `center`\n\n</details>\n\n\n\n----------------------------------------------------------------------------------------------------------\n\n\n\n## API\n\nsignalepy.`<logger>(message="", prefix="", suffix="")`\n\n<br>\n\n`logger`\n\n- Type: `function`\n\nCan be any default logger\n\n<br>\n\n`message`\n\n- Type: `str`\n\nMessage to be displayed\n\n<br>\n\n`prefix`\n\n- Type: `str`\n- Required: False\n\nPrefix text\n\n<br>\n\n`suffix`\n\n- Type: `str`\n- Required: False\n\nSuffix text\n\n\n\n----------------------------------------------------------------------------------------------------------\n\n\n\n**Licensed Under [MIT License](https://github.com/ShardulNalegave/signale.py/blob/master/LICENSE)**\n**A Project By [Shardul Nalegave](https://shardul.netlify.com)**',
    'author': 'Shardul Nalegave',
    'author_email': 'nalegaveshardul40@gmail.com',
    'url': 'https://github.com/ShardulNalegave/signale.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
