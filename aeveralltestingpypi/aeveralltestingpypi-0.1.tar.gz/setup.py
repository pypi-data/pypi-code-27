from setuptools import setup, find_packages

long_description = \
"""
Testing to see what we can do with Python Package Index
"""

setup(
    name="aeveralltestingpypi",
    version='0.1',
    
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['numpy'],

    package_data={'': ['*.md']
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },

    packages = ['script'],

    # metadata for upload to PyPI
    author="Andrew Everall",
    author_email="andrew.everall1995@gmail.com",
    description="Test of PyPI",
    license="GPLv3"  # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
