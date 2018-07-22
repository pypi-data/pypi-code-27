import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moonshade",
    version="0.0.1",
    author="KINA Open",
    author_email="open@kina.moe",
    description="A Universal Distributed Data Collection Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kinaopen/moonshade",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ),
)
