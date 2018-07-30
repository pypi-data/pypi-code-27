import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nftl_ed_lms_tools",
    version="0.1.4",
    author="Grzegorz Pawełczuk",
    author_email="grzegorz.pawelczuk@nftlearning.com",
    description="Tool 4 partial Ed LMS API handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
