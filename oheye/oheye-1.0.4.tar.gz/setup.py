import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oheye",
    version="1.0.4",
    author="Modern Device",
    author_email="shawn@as220.org",
    description="A library for the Modern Device Oh Eye analog input board for Raspberry Pi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=['spidev', 'python-osc'],
    url="https://github.com/fluxly/oheye",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
