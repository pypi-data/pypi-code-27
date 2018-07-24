import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InterferencePackage",
    version="0.0.1",
    author="Stefan Richter",
    author_email="stefan.richter@physical-perception.de",
    description="A package for calculating incoherent (or coherent) diffractiom images from FELs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.physical-engine.de",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)