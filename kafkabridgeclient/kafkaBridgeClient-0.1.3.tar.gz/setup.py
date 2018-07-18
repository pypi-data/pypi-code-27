import setuptools
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kafkaBridgeClient",
    version=os.environ.get("CI_COMMIT_TAG"),
    author="Benjamin Lindberg",
    author_email="benjamin.lindberg@gmail.com",
    description="A package for using kafka-bridge to talk to kafka inside docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/benkibejs/kafka-bridge/audentes",
    packages=setuptools.find_packages(include=['kafkaBridgeClient']),
    install_requires=[
          'requests'
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
