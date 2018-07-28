import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linuxcmd",
    version="0.0.2",
    author="Aditya nk",
    author_email="adityank003@gmail.com",
    description="A Python tool to get linux commands results from remote servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Adityank003",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
)
