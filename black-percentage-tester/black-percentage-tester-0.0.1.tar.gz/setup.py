from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="black-percentage-tester",
    description="Black formatter percentage checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="Milan Suk",
    author_email="milan.suk@kiwi.com",
    install_requires=["black"],
    packages=["func"],
    scripts=["black-percentage-test"],
)
