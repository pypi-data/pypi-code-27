import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="gpu_optimize",
	version="2018.08.1",
	author="Jackson Sipple",
	author_email="jsipple@berkeley.edu",
	description="Drop-in replacement functions that run on NVIDIA GPUs, parallelized for speed",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Jackmastr/gpu-optimize.git",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent",
	)
)
