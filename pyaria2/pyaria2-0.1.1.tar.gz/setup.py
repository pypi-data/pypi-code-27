import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaria2",
    version="0.1.1",
    author="hschen",
    author_email="pypi@haisong.me",
    description="a naive aria2c rpc api lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/tinyproxy/pyaria2",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)