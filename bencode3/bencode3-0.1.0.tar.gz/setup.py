import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bencode3",
    version="0.1.0",
    author="hschen",
    author_email="pypi@haisong.me",
    description="a simple bencode lib for python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/tinyproxy/bencode3",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)