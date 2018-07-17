import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loggui",
    version="0.1.3",
    author="OctoNezd",
    author_email="nezd@protonmail.com",
    description="GUI handler for python logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/octonezd/loggui",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only"
    ),
    install_requires=["PyQt5"]
)