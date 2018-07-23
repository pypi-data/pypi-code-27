
from setuptools import setup, find_packages
from autographs import VERSION

# Get the README.
with open("./README.md", "r") as f:
    README = f.read()

with open("./CONTRIBUTING.md", "r") as f:
    CONTRIBUTING = f.read()

reqs = [
    "numpy",
    "pysal",
    "geopandas",
    "matplotlib"
]

setup(
    name="autographs",
    description="A collection of tools to make graph stuff easy.",
    long_description=README + "\n\n" + CONTRIBUTING,
    author="Metric Geometry and Gerrymandering Group",
    author_email="gerrymandr@gmail.com",
    url="https://github.com/gerrymandr/autographs",
    packages=find_packages(),
    version=VERSION
)
