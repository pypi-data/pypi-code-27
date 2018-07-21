import setuptools
from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setuptools.setup(
    name="titanium_rhythm",
    version="1.0.3",
    author="Ganesh Kathiresan",
    author_email="ganesh3597@gmail.com",
    description="Automatic id3 modifier .mp3 files",
    long_description=read_md('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/ganesh-k13/titanium-rhythm",
    packages=['titanium_rhythm'],
    package_dir = {'titanium_rhythm': 'titanium_rhythm/'},
    package_data={'titanium_rhythm': ['info/*.*', 'song_info/*.xml']},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
          'discogs_client == 2.2.1',
          'eyeD3 == 0.8.7',
          'pyacoustid == 1.1.5',
          'pytest == 3.6.1',
          'requests == 2.18.4',
          'setuptools == 38.6.0',
          'validators == 0.12.2',
      ],
)
