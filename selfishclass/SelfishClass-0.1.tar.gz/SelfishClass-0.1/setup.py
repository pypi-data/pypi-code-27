import setuptools
from m2r import convert

with open("README.md", "r") as f:
    long_description = convert(f.read())

setuptools.setup(
    name="SelfishClass",
    version="0.1",
    author="SawyerSteven",
    author_email="sawyerstevenk@gmail.com",
    description="A minimal alternative to dataclasses and python-attrs",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sawyersteven/SelfishClass",
    packages=setuptools.find_packages(),
    classifiers=(
		"Programming Language :: Python",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ),
)
