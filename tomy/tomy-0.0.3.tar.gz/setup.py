import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tomy",
    version="0.0.3",
    author="Tom Victor",
    author_email="vjtomvictor@gmail.com",
    description="Bunch of useful python codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tomvictor/tomy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)