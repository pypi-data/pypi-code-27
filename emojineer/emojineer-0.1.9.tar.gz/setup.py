import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("emojineer/requirements.txt", "r") as fh:
    requirements = fh.readlines()
requirements = [i.replace("\n", "") for i in requirements]

setuptools.setup(
    name="emojineer",
    version="0.1.9",
    author="kzkz potato",
    author_email="kzkz.ozn@gmail.com",
    description="emojineer for emojineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kzkzgit/emojineer",
    packages=["emojineer"],
    include_package_data=True,
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
