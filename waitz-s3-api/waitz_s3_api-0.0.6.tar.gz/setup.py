import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="waitz_s3_api",
    version="0.0.6",
    author="Daniel Fritsch",
    author_email="dfritsch99@gmail.com",
    description='API created by Waitz that provides useful functionality to read and write from AWS S3.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Waitz-Inc/waitz_s3_api',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
