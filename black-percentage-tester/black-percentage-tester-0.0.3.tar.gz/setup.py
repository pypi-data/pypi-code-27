from setuptools import setup
from black_percentage_tester.__main__ import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="black-percentage-tester",
    description="Black formatter percentage checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    author="Milan Suk",
    author_email="milan.suk@kiwi.com",
    install_requires=["black"],
    packages=["black_percentage_tester"],
    entry_points={
        "console_scripts": [
            "black-percentage-test=black_percentage_tester.__main__:main"
        ]
    },
)
