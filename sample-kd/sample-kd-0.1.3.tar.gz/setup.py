import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sample-kd",
    version="0.1.3",
    author="Jefung",
    author_email="jefung865424525@gmail.com",
    description="sample data and analysis",
    long_description="",
    url="https://github.com/KD-Group/Half.Sample",
    packages=["sample"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    data_files=[('cpp_build/sample.exe')]
)
