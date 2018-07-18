import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sunuse",
    version="0.0.3",
    author="sunfudong",
    author_email="2498720718@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)