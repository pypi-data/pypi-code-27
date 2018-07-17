import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="softposit",
    version="0.0.1",
    author="Siew Hoon LEONG (Cerlane)",
    author_email="cerlane@posithub.org",
    description="SoftPosit Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cerlane/SoftPosit",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
