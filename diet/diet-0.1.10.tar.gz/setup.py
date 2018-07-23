import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = ["dash-api-python-client", "dash-auth-python-client", "requests_oauthlib"]

setuptools.setup(
    name="diet",
    version="0.1.10",
    author="Alexander Burgett",
    author_email="alex.burgett@sprga.com.au",
    description="Dash Import Export Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIRES,
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['diet = diet.__main__:main']},
    url="https://bitbucket.org/sporga/diet",
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)