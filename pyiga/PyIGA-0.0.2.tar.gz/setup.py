import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyIGA",
    version="0.0.2",
    author="Hoang-Giang Bui",
    author_email="giang.bui@rub.de",
    description="Isogeometric analysis in Python. Built upon KratosMultiphysics Kernel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vryy/isogeometric_application",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)



