import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bthomehub5-devicelist",
    version="0.1.1",
    author="Arran Hobson Sayers",
    author_email="ahobsonsayers@gmail.com",
    description="A library that returns a list of devices currently connected to a BT Home Hub 5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahobsonsayers/bthomehub5-devicelist",
    packages=setuptools.find_packages(),
    install_requires=['html-table-parser-python3==0.1.5', 'requests'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)