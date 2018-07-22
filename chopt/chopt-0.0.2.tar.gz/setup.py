import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chopt",
    version="0.0.2",
    author="Toby Slight",
    author_email="tobyslight@gmail.com",
    description="Choose options from a list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/chopt",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'chopt = chopt.__main__:main',
        ],
    }
)
