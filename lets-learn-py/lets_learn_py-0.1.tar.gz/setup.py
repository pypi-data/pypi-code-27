from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='lets_learn_py',
        version='0.1',
        description='Welcome to the User',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/learn-with-abhi/lets_learn_py',
        author='Abhilash R',
        author_email='smile_with_abhi@hotmail.com',
        licence='MIT',
        packages=find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ),
        )
