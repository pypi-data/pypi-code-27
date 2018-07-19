import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="lgad",
    version="0.0.5",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Simulator for the LGAD detector.",
    long_description="Simulator for the LGAD detector.",
    long_description_content_type="text/markdown",
    url="https://github.com/Tsangares/LGAD_SIM",
    package_data={'lgad': ['plates.json']},
    scripts=['lgad/moving_plates.py', 'lgad/test.py', 'lgad/simulation.py'],
    extras_require={
        "matplotlib": ["matplotlib"]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
