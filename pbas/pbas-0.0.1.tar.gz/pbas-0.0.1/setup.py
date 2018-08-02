import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


PACKAGE = "pbas"
NAME = "pbas"
DESCRIPTION = "Simple web server with basic authentication"
AUTHOR = "Slava Beloglazov"
AUTHOR_EMAIL = "beloglazov.v.d@gmail.com"
URL = "https://github.com/beloglazof/pbs"
VERSION = "0.0.1"


setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
    ],
)
