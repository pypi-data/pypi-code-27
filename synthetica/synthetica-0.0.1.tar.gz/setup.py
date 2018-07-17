import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synthetica",
    version="0.0.1",
    author="Synthetica Dev Team",
    author_email="dev@mail.synthetica.bio",
    description="A client for synthetica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synthetica-bio/synthetica",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
