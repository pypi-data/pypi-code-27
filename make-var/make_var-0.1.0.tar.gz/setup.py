import setuptools

with open("Readme.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="make_var",
    version="0.1.0",
    author='Tony Karnigen',
    author_email='karnigen@gmail.com',
    description='Retrieve all variables defined by make command',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='http://github.com/karnigen/make_var',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

