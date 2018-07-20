import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JVP",
    version="0.0.1",
    author="Jerome Petit",
    author_email="jerome.petit@finastra.com",
    description="A first draft of JVP tools",
    install_requires=['pandas','numpy','matplotlib','eikon'],
    packages=setuptools.find_packages(),
)