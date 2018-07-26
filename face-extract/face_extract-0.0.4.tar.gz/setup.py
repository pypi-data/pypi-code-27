import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="face_extract",
    version="0.0.4",
    author="Anupam Jain",
    author_email="anupam124jain@gmail.com",
    description="You can extract face in user identity image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['opencv-python==3.4.2.17'],
    packages=setuptools.find_packages(),

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)