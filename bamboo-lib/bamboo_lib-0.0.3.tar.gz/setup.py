import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bamboo_lib",
    version="0.0.3",
    author="Jonathan Speiser",
    license='All Rights Reserved',
    author_email="jonathan@datawheel.us",
    description="Python ETL library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Datawheel/bamboo-lib",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
