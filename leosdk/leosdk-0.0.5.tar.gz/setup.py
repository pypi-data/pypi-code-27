import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leosdk",
    version="0.0.5",
    author="Monty Charlton",
    license="MIT",
    author_email="mcharlton@leoinsights.com",
    description="Python SDK for the Leo Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoPlatform/python",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True
)
