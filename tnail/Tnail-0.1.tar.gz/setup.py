from setuptools import setup, find_packages

setup(
    name="Tnail",
    version='0.1',
    description='Package with common operations on image.',
    author='Abhishek Chomal',
    packages=find_packages(),
    install_requires=['wand', ],
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
