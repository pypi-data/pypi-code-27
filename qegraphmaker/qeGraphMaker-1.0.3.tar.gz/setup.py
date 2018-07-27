import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qeGraphMaker",
    version="1.0.3",
    author="Kevin Postlethwait",
    author_email="kpostlet@redhat.com",
    description="Create PDF Graphs from Google Sheets Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KPostOffice/QETool_pip",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
      'requests',
      'matplotlib',
    ],
    entry_points = {
        'console_scripts': [
            'fileMaker=qeGraphMaker.createFile:main',
            'graphGen=qeGraphMaker.xeqt:main'
        ]
    },
)
