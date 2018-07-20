from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TTCPy',
    version="0.2.0",
    author='Eric Herwin',
    description='Make a list of strings to frequency of words',
    author_email = 'herwineric@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url= "https://github.com/herwineric/Portfolio",
    license='MIT',
    install_requires=['numpy', 'numba'],
    python_requires='>=3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Editors :: Text Processing",
    ),
)
