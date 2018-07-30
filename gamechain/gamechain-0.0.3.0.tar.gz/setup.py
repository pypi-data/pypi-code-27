import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamechain",
    version="0.0.3.0",
    author="Albert Boehmler",
    author_email="ajboehmler@gmail.com",
    description="Protocol for playing, recording, and watching games on the BCH blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devalbo/gamechain-py",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=["socketIO-client"]
)