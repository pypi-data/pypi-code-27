import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazier",
    version="0.0.1",
    author="Arjun Srivastava",
    author_email="arjunbazinga@gmail.com",
    description="Lazier workflow for Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arjunbazinga/lazier",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)