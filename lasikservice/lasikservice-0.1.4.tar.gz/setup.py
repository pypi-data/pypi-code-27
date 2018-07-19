import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lasikservice",
    version="0.1.4",
    author='sasja',
    author_email='sasja.ws@gmail.com',
    description='connects to a number of lasik boards and provides a service',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/sasja/lasik',
    packages=setuptools.find_packages(),
    install_requires=['pyserial'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ),
    entry_points={
        'console_scripts': [
            'lasikservice = lasikservice.service:main',
            'lasikconnect = lasikservice.serialconnection:main',
        ],
    },
)
