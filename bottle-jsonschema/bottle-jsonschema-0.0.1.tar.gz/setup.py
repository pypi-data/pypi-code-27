
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="bottle-jsonschema",
    version="0.0.1",
    author="Tomas Sandven",
    author_email="tomas191191@gmail.com",
    description="Automatic JSON schema validation for Bottle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hubro/bottle-jsonschema",
    py_modules=["bottle_jsonschema"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
