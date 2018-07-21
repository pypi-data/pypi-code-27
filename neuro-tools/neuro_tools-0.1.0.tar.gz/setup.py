import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neuro_tools",
    version="0.1.0",
    author="Bruno Melo",
    author_email="bruno.melo@idor.org",
    description="Neuroimaging tools to help with BIDS, XNAT, workflows, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/InstitutoDOr/neuro_tools",
    packages=setuptools.find_packages(),
    install_requires=[
          'pydicom',
          'openpyxl',
          'xnat',
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)