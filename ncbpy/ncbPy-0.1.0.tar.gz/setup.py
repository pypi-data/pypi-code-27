import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ncbPy",
    version="0.1.0",
    author="Josué Caleb",
    author_email="josuecaleb09@hotmail.com",
    description="A small module to scrape ncbi nucleotide sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JCalebBR/ncbPy/",
    packages=setuptools.find_packages(),
    install_requires=[
          'beautifulsoup4',
          'tqdm',
          'selenium'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: Portuguese (Brazilian)",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)