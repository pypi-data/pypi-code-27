import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minglight",
    version="1.0.3",
    author="周明明",
    author_email="1159922370@qq.com",
    description="a server build with socket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Silence-ming/myFlask.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)