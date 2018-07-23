import setuptools

MAJOR = 0
MINOR = 1
PATCH = 0
VERSION = '{}.{}.{}'.format(MAJOR, MINOR, PATCH)

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="multisite",
        version=VERSION,
        author="Corey McCandless",
        author_email="crm1994@gmail.com",
        description=(
            "Host multiple standalone websites under a single site"
        ),
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/cmccandless/multisite",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        entry_points={
            'console_scripts': [
                'multisite = multisite.__main__:main'
            ],
        },
        install_requires=['argutil']
    )
