import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portiapy",
    version="0.1.1",
    author="Matheus Mota",
    author_email="matheus@agrinessedge.com",
    description="A small package for handling Agriness Edge rest API",
    long_description=long_description,
    url="https://github.com/agrinessedge/edge-playground",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)