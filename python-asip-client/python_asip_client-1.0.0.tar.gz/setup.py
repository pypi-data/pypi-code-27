from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python_asip_client",
    version="1.0.0",
    author="Gianluca Barbon, Adam Jarzebak, Franco Raimondi",
    author_email="adam@jarzebak.eu",
    description="Serial manager for Mirto robot services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdxmase/mirto_python_asip",
    packages=['python_asip_client'],
    # packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
)
