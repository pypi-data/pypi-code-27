import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysuper",
    version="0.2.91",
    author="James Collier",
    author_email="james@thecolliers.xyz",
    description="Search for oligopeptide fragments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/structural-fragment-search/super",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["pysuper/build_pysuper.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
    packages=["pysuper"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    )
)
