import setuptools
import re

with open("README.rst", "r") as fh:
    # long_description = re.sub('^\.\. highlight.*\n?', '', fh.read(), flags=re.MULTILINE)
    long_description = fh.read()

setuptools.setup(
    name="cryptostream",
    version_format="{tag}",
    author="David Jablonski",
    author_email="dayjaby@gmail.com",
    description="Stream data to multiple clients whilst respecting privacy of the data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/dayjaby/cryptostream",
    packages=setuptools.find_packages(),
    install_requires=['pycryptodome'],
    setup_requires=['setuptools-git-version'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
