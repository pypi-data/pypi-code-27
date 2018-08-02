import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_adb_utils",
    py_modules=['python_adb_utils'],
    version="0.0.9",
    author="Christopher Ferreira",
    author_email="christopher.ferreira3@outlook.com",
    description="This is the first test of a ADB interface for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christopherferreira3/Python-ADB-Tools",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)