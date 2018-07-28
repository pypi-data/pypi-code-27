from setuptools import setup
import setuptools
import src

setup(
    name='studious-octo-parakeet',
    version=src.__version__,
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description_content_type="text/markdown",
    url="https://github.com/marionlb/studious-octo-parakeet",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
