import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lasikservice",
    version="0.1.1",
    author='sasja',
    author_email='sasja.ws@gmail.com',
    description='connects to a number of lasik boards and provides a service',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/sasja/lasik',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ),
    entry_points={
        'consose_scripts': [
            'lasikservice = lasikservice.service',
            'lasikconnect = lasikserivce.serialconnection',
        ],
    },
)
