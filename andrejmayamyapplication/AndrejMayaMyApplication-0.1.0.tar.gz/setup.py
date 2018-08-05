from distutils.core import setup

setup(
    # Application name:
    name="AndrejMayaMyApplication",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Andrej Maya",
    author_email="andrej@googlemail.br",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/AndrejMayaMyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)