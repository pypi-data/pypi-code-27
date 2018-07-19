import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pestcontrol",
    version="1.0.5",
    author="Luke Baal",
    author_email="lukebaal2020@gmail.com",
    description="A Python unit testing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/LukeBaal/PestControl",
    packages=setuptools.find_packages(),
    install_requires=[
      'colorama'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)