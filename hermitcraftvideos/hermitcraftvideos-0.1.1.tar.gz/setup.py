import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hermitcraftvideos",
    version="0.1.1",
    author="SamHDev",
    author_email="samhdev@gmail.com",
    description="A Wrapper for Hermicraft Video API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SamHDev/Hermitcraft-Video-Api",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
