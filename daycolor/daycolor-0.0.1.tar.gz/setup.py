import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="daycolor",
    version="0.0.1",
    author="David Huss",
    author_email="dh@atoav.com",
    description="Return a interpolated RGB color depending on the time of the day",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atoav/daycolor",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)