import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liandan",
    version="0.0.0",
    author="ahhuang",
    author_email="contact@huanganheng.com",
    description="A package for LIANDAN tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anhenghuang/liandan",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)