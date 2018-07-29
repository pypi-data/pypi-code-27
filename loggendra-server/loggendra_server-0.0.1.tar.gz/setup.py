import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loggendra_server",
    version="0.0.1",
    author="Tushar Pawar",
    author_email="gmail@tusharpawar.com",
    description="Centralised server for storing server logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Backalla/loggendra-server",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)