import setuptools

import cutt_sd

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=cutt_sd.name,
    version=cutt_sd.version,
    author="YHC",
    author_email="chenyonghui@gmail.com",
    description="zk service discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ourbest/cutt_sd",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'kazoo', 'flask'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
