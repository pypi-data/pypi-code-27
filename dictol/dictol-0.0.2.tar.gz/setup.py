import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    include_package_data=True,
    name="dictol",
    version="0.0.2",
    author="Tiep Vu",
    author_email="vuhuutiep@gmail.com",
    description="A dictionary learning package for classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiepvupsu/dictol_python",
    packages=['dictol'],
    package_dir = {'dictol': 'dictol'},
    parkage_data={'dictol':['data/*.mat']},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
