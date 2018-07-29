import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atgcN_count",
    version="0.0.1",
    author='Guanliang Meng',
    author_email='mengguanliang@foxmail.com',
    description="To stat the counts and percentage of each base in fasta file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    url='https://github.com/linzhi2013',
    packages=setuptools.find_packages(),
    include_package_data=True,
    # install_requires=[''],

    entry_points={
        'console_scripts': [
            'atgcN_count=atgcN_count.atgcN_count:main',
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