from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='verse',
    version='1.7',
    packages=['versesrc'],
    url='https://github.com/ethanquix/verse',
    license='MIT',
    author='dwyzlic',
    author_email='dimitriwyzlic@gmail.com',
    description='Verse allow you to define easy instruction and commands for each of your project !',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'verse=versesrc:main',
        ],
    },

)
