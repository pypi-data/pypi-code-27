from setuptools import setup

__project__ = "dandipy"
__version__ = "0.0.2"
__description__ = "A python module to access @chattered D&D RESTful API"
__packages__ = ["dandipy"]
__author__ = "Marc Scott"
__author_email__ = "marc@coding2learn.org"
__install_requires__ = ["requests"]
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    install_requires = __install_requires__,
    )
