import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leftpad",
    version="0.1.2",
    author="James Cagalawan",
    author_email="james.cagalawan@gmail.com",
    description="A port of the infamous left-pad npm package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cglwn/leftpad-pypi",
    py_modules=['leftpad'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)