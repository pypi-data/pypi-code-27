import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_catapult",
    version="0.0.3",
    author="Jonathan Speiser",
    author_email="jonathan@datawheel.us",
    description="Python bulk data loading ETL library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Datawheel/catapult",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
