import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="videoCrawler",
    version="0.0.1",
    author="Ayush21298",
    author_email="patel.ayush08@gmail.com",
    description="Crawl Video from Youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayush21298/ITRI/tree/master/videoCrawler",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)