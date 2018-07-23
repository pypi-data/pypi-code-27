import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="billionfong",
    version="1.0.0",
    author="Billy Fong",
    author_email="billionfong@billionfong.com",
    description="Welcome to my package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.billionfong.com/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)