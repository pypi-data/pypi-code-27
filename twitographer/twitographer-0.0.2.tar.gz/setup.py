import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitographer",
    version="0.0.2",
    author="liveb33f",
    author_email="livebeef@protonmail.com",
    description="A parallelized web crawler to traverse the Twitter graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liveb33f/twitographer",
    packages=setuptools.find_packages(),
    license='unlicense',
    install_requires=[
        'pyppeteer>=0.0.19',
        'redis>=2.10.6',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
    ),
)
