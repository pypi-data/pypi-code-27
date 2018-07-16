import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="active_learning",
    version="0.2.3",
    author="Lucas Rosen, Hossein Soleimani, Tony Wang",
    author_email="lrosen27@jhu.edu",
    description="Active Learning With Rich feedabck",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonywang124/TREWS-AL",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

