# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['signalepy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'signalepy',
    'version': '0.2.0',
    'description': 'Elegant Console Logger For Python Command Line Apps',
    'long_description': '\n<div align="center" id="main">\n\t<h1 align="center">Signale.py</h1>\n\t<p align="center">Elegant Console Logger For Python Command-Line Apps</p>\n\t<br>\n\t<br>\n\t<img src="./imgs/main.png" alt="example" align="center">\n</div>\n\n<hr>\n\n\n\n## Installation\n**Signale.py** can be installed using pip.\n\n````bash\n\n    [sudo] pip install signalepy\n\n````\n\n\n\n## Usage\nPackage consists of a class `Signale`, it is the main constructor class. The object created has all the logger functions in it.\n\n\n### Using Loggers\nEach logger function takes in three arguments:-\n- `text`\n- `prefix` ( Optional )\n- `suffix` ( Optional )\n\nThey all are available in the logger object. To create one do this:-\n````python\n\n    from signalepy import Signale\n\n    logger = Signale()\n\n````\n\nNow you can use the default loggers using this object like:-\n````python\n\n    ...\n\n\tlogger.success("Started Successfully", prefix="Debugger")\n\tlogger.warning("`a` function is deprecated", suffix="main.py")\n\tlogger.complete("Run Complete")\n\n    ...\n\n````\n\n\nThis will produce the following result:-\n\n<div align="center">\n\t<img align="center" src="./imgs/result.png">\n</div>\n\n<br><br>\n\n<details>\n\t<summary>View All Available Loggers</summary>\n\n- `simple`\n- `success`\n- `error`\n- `warning`\n- `start`\n- `stop`\n- `watch`\n- `important`\n- `pending`\n- `complete`\n- `debug`\n- `pause`\n- `info`\n- `like`\n- `center`\n\n</details>\n\n\n\n----------------------------------------------------------------------------------------------------------\n\n\n\n## Scoped Loggers\nTo create scoped loggers, define the `scope` field in the `options` argument of constructor like:-\n\n````python\n\n\tfrom signalepy import Signale\n\n    logger = Signale({\n    \t"scope": "global scope"\n    })\n    logger.success("Scoped Logger Works!")\n\n````\n\nThis will produce the following result:-\n\n<div align="center">\n\t<img src="./imgs/scope_str.png" align="center">\n</div>\n\n<br><br>\n\nYou also create multiple scopes by setting the `scope` field to a list of strings like:-\n\n````python\n\n\tfrom signalepy import Signale\n\n    logger = Signale({\n    \t"scope": ["global scope", "inner scope"]\n    })\n    logger.success("Scoped Logger Works!")\n\n````\n\nThis will produce the following result:-\n\n<div align="center">\n\t<img src="./imgs/scope_list.png" align="center">\n</div>\n\n\n----------------------------------------------------------------------------------------------------------\n\n\n\n## API\n\n1. logger = `Signale(<options>)`\n\n\t<br>\n\n\t`Signale`\n\n\t- Type: `class`\n\n\tSignale class imported from `signalepy` module\n\n\t<br>\n\n\t`options`\n\n\t- Type: `dict`\n\n\tOptions Dictionary for logger.\n\n\t<br><br>\n\n2. logger.`<logger>(message="", prefix="", suffix="")`\n\n\t<br>\n\n\t`logger`\n\n\t- Type: `function`\n\n\tCan be any default logger\n\n\t<br>\n\n\t`message`\n\n\t- Type: `str`\n\n\tMessage to be displayed\n\n\t<br>\n\n\t`prefix`\n\n\t- Type: `str`\n\t- Required: False\n\n\tPrefix text\n\n\t<br>\n\n\t`suffix`\n\n\t- Type: `str`\n\t- Required: False\n\n\tSuffix text\n\n\n\n----------------------------------------------------------------------------------------------------------\n\n\n\n**Licensed Under [MIT License](https://github.com/ShardulNalegave/signale.py/blob/master/LICENSE)**\n**A Project By [Shardul Nalegave](https://shardul.netlify.com)**',
    'author': 'Shardul Nalegave',
    'author_email': 'nalegaveshardul40@gmail.com',
    'url': 'https://github.com/ShardulNalegave/signale.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
