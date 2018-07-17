import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toro-shortcuts",
    version="1.1",
    author="Steven Larry Ball",
    author_email="stevenlarry.ball@torocloud.com",
    description="A Python Markdown extension for keyboard shortcuts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.torocloud.com/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    py_modules=['toro-shortcuts'],
)
