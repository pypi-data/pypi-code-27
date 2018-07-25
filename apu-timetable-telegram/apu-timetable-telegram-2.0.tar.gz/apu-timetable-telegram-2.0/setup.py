import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="apu-timetable-telegram",
	version="2.0",
	author="Low Yiyiu",
	author_email="lowyiyiu@gmail.com",
	description="A Telegram bot for students of Asia Pacific University of Technology and Innovation to view their timetable",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/lowyiyiu/APU-Timetable-Telegram",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
)