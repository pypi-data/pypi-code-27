import os
import setuptools
# from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "takahiroHelloWorld",
    version = "1.0.3",  # major, minor, micro
    author = "sakurai",
    author_email = "sakurai@gamil.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = (
        "Programming Language :: Python :: 3.3", 
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
    zip_safe = False,
    entry_points = {
        "console_scripts": [
            "my_say_hello = helloWorld.hello:main",
        ]
    }
)
