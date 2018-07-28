import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SpectDetect",
    version="0.0.1",
    author="Tom Hudson",
    description="Microseismic detection algorithm package based on using key features in the spectrum of a source to detect earthquakes over a given time period.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomSHudson/SpectDetect",
    packages=['SpectDetect'],
    license='MIT',
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
