# chardet's setup.py
from distutils.core import setup
setup(
    name = "hoddb",
    packages = ["hoddb"],
    version = "0.0.1",
    description = "HodDB Python Client",
    author = "Gabe Fierro",
    author_email = "gtfierro@eecs.berkeley.edu",
    url = "https://hoddb.org",
    install_requires=[
        'requests',
        'rdflib'
    ]
)
