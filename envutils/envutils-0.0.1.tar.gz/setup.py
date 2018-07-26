import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="envutils",
    version="0.0.1",
    author="Matteo Filipponi",
    author_email="matteofilipponi@hotmail.com",
    description="A python library to read and parse environment variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mfilippo/envutils",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
