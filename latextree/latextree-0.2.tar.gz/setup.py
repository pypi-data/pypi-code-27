from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='latextree',
    version='0.2',
    description='A document object model and related tools for Latex',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/cardiffmaths/latextree',
    author='D Evans',
    author_email='evansd8@cf.ac.uk',
    license='MIT',
    packages=['latextree'],
    install_requires=[
        'jinja2',
        'pylatexenc',
        'bibtexparser',
        'lxml',
        'six',
    ],
    entry_points = {
        'console_scripts': ['ltree=latextree.ltree:main'],
    },
    zip_safe=False,
)
