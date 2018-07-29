from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python_asip_client",
    version="1.0.5",
    author="Gianluca Barbon, Adam Jarzebak, Michael Margolis, Franco Raimondi",
    author_email="adam@jarzebak.eu",
    description="Serial manager for Mirto robot services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdxmase/mirto_python_asip",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
)
