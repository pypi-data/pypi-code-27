import setuptools
from api_builder import configuration

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-lambda-api-builder",
    version=configuration.VERSION,
    author="Zachary Miller",
    author_email="me@zackmiller.info",
    description="Build and deploy AWS API Gateways using AWS Lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zmiller91/python-lambda-packager",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points = {
        'console_scripts': [
            'zlab=api_builder.zlab:main'
        ]
    },
      install_requires=[
          'pipenv', 'boto3', 'pystache', 'botocore'
      ],
)