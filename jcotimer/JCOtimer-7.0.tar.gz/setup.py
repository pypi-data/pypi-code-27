import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JCOtimer",
    version="7.0",
    author="Jan Carlo Once",
    author_email="jancarloonce11@gmail.com",
    description="JCOtimer is a Python utility/package for measuring function runtime.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jancarloonce/JCOtimer",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
