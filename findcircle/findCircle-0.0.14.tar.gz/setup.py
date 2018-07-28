import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="findCircle",
    version="0.0.14",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Find the max intercept of circles.",
    long_description="Find the max intercept of circles.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/findCircle",
    install_requires=["matplotlib", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
