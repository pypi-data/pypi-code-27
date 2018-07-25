from setuptools import setup

TITLE = "tocamelcase"
VERSION = "0.0.6"
SUMMARY = "🐫 To Camel Case: self explanatory!"
LIC = "MIT"

AUTHOR_NAME = "Carlos Abraham"
AUTHOR_MAIL = "abraham@abranhe.com"

with open("README.md", "r") as d:
    LONG_DESCRIPTION = d.read()

setup(
    name=TITLE,
    packages = ["tocamelcase"],
    version=VERSION,
    description=SUMMARY,
    author=AUTHOR_NAME,
    author_email=AUTHOR_MAIL,
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/abranhe/tocamelcase/',
    },
    license=LIC,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Plugins",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)
