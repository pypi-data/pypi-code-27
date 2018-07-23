import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLme",
    version="0.0.101",
    author="Pisek Kultavewuti",
    author_email="psk.light@gmail.com",
    description="tools to work on machine learning and data science projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psklight/MLme",
    packages=setuptools.find_packages(),
    install_requires=['numpy','pandas'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)