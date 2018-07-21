import setuptools

setuptools.setup(
    name='burnytestlib',    # This is the name of your PyPI-package.
    author="Burny",
    author_email="gamingburny@gmail.com",
    url="https://github.com/BurnySc2/testing-stuff",
    version='0.0.1',                          # Update the version number for new releases
    # scripts=['burnytestlib']                  # The name of your scipt, and also the command you'll be using for calling it
    description="A small example package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    packages=["burnytestlib"]
)