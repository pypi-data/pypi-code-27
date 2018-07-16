try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    name="cfman",
    description="CFMan Pages for Status Codes",
    version="v2.0.2",
    install_requires=["pyyaml", "urwid"],
    packages=["cfman"],
    entry_points={"console_scripts": ["cfman = cfman.cfman:main"]},
    include_package_data=True,
    python_requires=">=2",
    url="https://github.com/farberjd/cfman",
    author="farberjd",
    author_email="farber911@gmail.com",
    license="MIT"
)
