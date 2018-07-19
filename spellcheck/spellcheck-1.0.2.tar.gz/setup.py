import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spellcheck",
    version="1.0.2",
    description="Simple spellcheck tool",
	author='Polloz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LilChickenz/spellcheck",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
