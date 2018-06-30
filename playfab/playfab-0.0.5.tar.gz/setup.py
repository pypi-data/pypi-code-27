import setuptools
with open("README.md", "r") as fh:
        long_description = fh.read()
        
setuptools.setup(
    name="playfab",
    version="0.0.5",
    author="PlayFab Dev Tools team",
    author_email="devrel@playfab.com",
    description="PlayFab Python SDK current API version: 0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PlayFab/PythonSdk",
    project_urls={"DocsURL": "https://api.playfab.com/", "SupportURL": "https://community.playfab.com/index.html", "CreatedByURL": "https://playfab.com/"},
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ),
)
