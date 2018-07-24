import os
from setuptools import setup, find_packages
from importlib.machinery import SourceFileLoader


# load aio_timers/version.py
module = SourceFileLoader("version", os.path.join("aio_timers", "version.py")).load_module()

setup(
    name='aio-timers',
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.package_license,
    description=module.package_info,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=module.__repo__,
    platforms="all",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.5.*, <4"
)
