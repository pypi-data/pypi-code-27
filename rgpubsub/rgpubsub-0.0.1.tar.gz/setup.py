from setuptools import setup

setup(
    name='rgpubsub',
    version='0.0.1',
    packages=['rgpubsub',],
    author="Eirik Tenold",
    description="Simple helper utility to send Google Pubsub messages easily",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ),
)