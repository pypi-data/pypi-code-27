import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()
print(setuptools.find_packages())
setuptools.setup(
    name="lgad",
    version="0.0.13",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Simulator for the LGAD detector.",
    long_description="Simulator for the LGAD detector.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages() + ['lgad/bin'],
    url="https://github.com/Tsangares/LGAD_SIM",
    package_data={'lgad': ['plates.json']},
    extras_require={
        "matplotlib": ["matplotlib"]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
