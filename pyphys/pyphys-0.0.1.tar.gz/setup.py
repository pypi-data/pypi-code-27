import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyphys",
    version="0.0.1",
    author="Orens Xhagolli",
    author_email="orens.xhagolli@hotmail.com",
    description="pygame based physics engine for better 2D simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oxhagolli/pyphys",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
