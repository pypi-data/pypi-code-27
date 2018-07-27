import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="PyRiddim",
	version="0.0.1",
	author="Andy Friedman",
	author_email="afriedman412@gmail.com",
	description="A totally unofficial Python wrapper for Riddimbase.org",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/afriedman412/PyRiddim",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
)