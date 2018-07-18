import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="nginxaccesslogparser",
	version="0.8.0",
	author="Kaustubh Olpadkar",
	author_email="kaustubh.olpadkar@gmail.com",
	description="nginx access log parser",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kaustubholpadkar/nginx-access-log-parser-Python",
	packages=setuptools.find_packages(),
	install_requires=['terminaltables'],
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		),
	entry_points={
        'console_scripts': [
        	'nginxaccesslogparser = nginxaccesslogparser.nginxaccesslogparser:main',
        ],
    },
)
