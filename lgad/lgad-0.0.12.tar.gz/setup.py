import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="lgad",
    version="0.0.12",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Simulator for the LGAD detector.",
    long_description="Simulator for the LGAD detector.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/LGAD_SIM",
    package_data={'lgad': ['plates.json'], 'lgad/bin': ['lgad']},
    extras_require={
        "matplotlib": ["matplotlib"]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
