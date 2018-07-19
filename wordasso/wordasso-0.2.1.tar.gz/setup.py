import setuptools
import codecs
import os


def local_file(file):
    return codecs.open(os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8')


install_reqs = [line.strip() for line in local_file('requirements.txt').readlines() if line.strip() != '']


setuptools.setup(
    name="wordasso",
    version="0.2.1",
    author="Author",
    author_email="martibook@outlook.com",
    description="Several word association function based on datamuse API",
    long_description=local_file('README.md').read(),
    url="https://github.com/martibook/wordasso.git",
    install_requires=install_reqs,
    packages=["wordasso"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
