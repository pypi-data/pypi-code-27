import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nessusha",
    version="0.3.0",
    author="Li Xingxuan",
    author_email="lxx895466249@gmail.com",
    description="Extract Nessus HA data to xlsx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SanPersie",
    packages=setuptools.find_packages(),
    install_requires=[
        "bs4",
        "xlsxwriter"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)