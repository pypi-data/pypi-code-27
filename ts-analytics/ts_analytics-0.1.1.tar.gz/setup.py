from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "ts_analytics",
    version = "0.01.1",
    author="Eneliko Mulokozi",
    author_email = "emulokozi@aol.com",
    description = "Traffic data analytics",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/pypa/ts_project",
    packages = find_packages(),
    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)