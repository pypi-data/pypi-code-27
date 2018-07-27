import setuptools

REQUIRED_PACKAGES = [
    'googleapis-common-protos >= 1.5.3',
    'grpcio == 1.13.0',
]

TEST_PACKAGES = [
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moonshade",
    version="0.0.2",
    author="Kina Wakasa",
    author_email="wakasakina@gmail.com",
    description="A Universal Distributed Data Collection Framework",
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES + TEST_PACKAGES,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kinaopen/moonshade",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ),
)
