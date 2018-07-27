try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from electrician import version

config = {
    'description': 'An abstraction layer to control GPIO devices connected to a raspberry pi',
    'author': 'Brandon Myers',
    'url': 'https://github.com/pwnbus/electrician',
    'download_url': 'https://github.com/pwnbus/electrician/archive/master.zip',
    'author_email': 'pwnbus@mozilla.com',
    'version': version,
    'packages': ['electrician'],
    'scripts': [],
    'name': 'electrician'
}

setup(**config)
