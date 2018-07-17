import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Jonathan Speiser",
    author_email="jonathan@datawheel.us",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    description="Python ETL library",
    install_requires=[
        "pandas",
        "sqlalchemy",
        "data-catapult",
        "paramiko",
        "sshtunnel",
        "redis"
    ],
    name="bamboo_lib",
    license='All Rights Reserved',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),

    version="0.0.5",

    url="https://github.com/Datawheel/bamboo-lib",


)
