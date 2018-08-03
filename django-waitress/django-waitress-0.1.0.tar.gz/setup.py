# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_waitress',
 'django_waitress.management',
 'django_waitress.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['waitress>=1.1,<2.0']

setup_kwargs = {
    'name': 'django-waitress',
    'version': '0.1.0',
    'description': 'Run a production-ready server from manage.py',
    'long_description': 'django-waitress\n===============\n\nRun a production-ready server from manage.py!\n\nThis Django app just provides a management command that serves your Django project using Waitress, a production-ready and `Heroku-friendly <heroku>`_ WSGI server.\n\n.. _heroku: http://blog.etianen.com/blog/2014/01/19/gunicorn-heroku-django/\n\nUsage\n-----\n\n.. code-block:: sh\n\n    # Serve on http://0.0.0.0:7000\n    python manage.py serve --host 0.0.0.0 --port 7000\n\n    # Serve on the Unix socket /var/run/myapp\n    python manage.py serve --unix /var/run/myapp\n\n    # Serve on the host defined by WAITRESS_HOST\n    # and the port defined by WAITRESS_PORT\n    # in settings.py\n    # (defaults to localhost:8000)\n    python manage.py serve\n\nAlternatives\n------------\n\nYou could just install Waitress itself, and run the ``waitress-serve`` command it provides, pointing to your ``wsgi.py`` file; the only thing that this project does is provide a Django management command, and remove the need for a ``wsgi.py`` in your project.\n\nLicense\n-------\n\nThis project was extracted from `CMV\'s cookiecutter-django <ccdj>`_\n\n.. _ccdj: https://gitlab.com/abre/cookiecutter-django\n\n.. raw:: html\n\n    <p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">\n        <a rel="license"\n            href="http://creativecommons.org/publicdomain/zero/1.0/">\n            <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />\n        </a>\n        <br />\n        To the extent possible under law,\n        <span resource="[_:publisher]" rel="dct:publisher">\n            <span property="dct:title">Commercial Motor Vehicles Pty Ltd</span></span>\n        have waived all copyright and related or neighboring rights to\n        <span property="dct:title">cookiecutter-django</span>.\n        This work is published from:\n        <span property="vcard:Country" datatype="dct:ISO3166"\n            content="AU" about="[_:publisher]">\n        Australia</span>.\n    </p>',
    'author': 'Adam Brenecki',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
