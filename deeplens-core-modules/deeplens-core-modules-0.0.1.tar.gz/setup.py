import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deeplens-core-modules",
    version="0.0.1",
    author="Paul Fryer",
    description="The core python modules needed to run Lambda functions on DeepLens devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulfryer/DeepLens",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)