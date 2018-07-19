import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypi_pkg_test",
    version="0.0.4",
    author="jasonqiao36",
    author_email="jasonqiao36@gmail.com",
    description="A small test about distrubution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasonqiao36/pypi-pkg-test",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
