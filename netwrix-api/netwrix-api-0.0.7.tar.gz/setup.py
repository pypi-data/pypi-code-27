import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netwrix-api",
    version="0.0.7",
    author="Cliff Hults",
    author_email="bongoeadgc6@gmail.com",
    description="A library to interact with Netwrix Search API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BongoEADGC6/netwrix-api",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "requests"
    ]
)
