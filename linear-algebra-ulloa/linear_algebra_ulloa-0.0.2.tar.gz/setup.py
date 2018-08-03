import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linear_algebra_ulloa",
    version="0.0.2",
    author="Luis Ulloa",
    author_email="ulloa@stanford.edu",
    description="Vector/Matrix classes - refined rref and fixed a bug. Added author information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ulloaluis/linear-algebra",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
