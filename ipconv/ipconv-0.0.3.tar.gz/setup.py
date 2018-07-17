import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipconv",
    version="0.0.3",
    author="Pranav Gajjewar",
    author_email="apbetahouse45@gmail.com",
    description="An easy and convenient IP address operation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cartmanishere/IPLib",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)