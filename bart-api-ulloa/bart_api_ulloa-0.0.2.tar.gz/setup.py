import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bart_api_ulloa",
    version="0.0.2",
    author="Luis Ulloa",
    author_email="ulloa@stanford.edu",
    description="bart api wrapper in python, now returns data instead of just printing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ulloaluis/bart-api-wrapper-python",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)