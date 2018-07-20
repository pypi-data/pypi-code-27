import setuptools

with open("README.md.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gscPack",
    version="0.0.0",
    author="Samuel Mansfield",
    author_email="samueljmansfield@gmail.com",
    description="This package assists in the creation and manipulation of gsc (Gravestroke Seperated Coloumns) files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Trek1492/gscPack",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ),
)
