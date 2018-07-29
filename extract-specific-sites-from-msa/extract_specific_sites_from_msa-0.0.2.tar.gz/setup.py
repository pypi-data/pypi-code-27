import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extract_specific_sites_from_msa",
    version="0.0.2",
    author='Guanliang Meng',
    author_email='mengguanliang@foxmail.com',
    description="To extract some sites from a multiple sequence alignment. By Guanliang MENG, go to https://github.com/linzhi2013 for more details.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    url='https://github.com/linzhi2013',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['biopython>=1.54'],

    entry_points={
        'console_scripts': [
            'extract_specific_sites_from_msa=extract_specific_sites_from_msa.extract_specific_sites_from_msa:main',
        ],
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ),
)