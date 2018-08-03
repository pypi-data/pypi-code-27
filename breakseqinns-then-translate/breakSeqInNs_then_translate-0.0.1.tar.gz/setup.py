import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="breakSeqInNs_then_translate",
    version="0.0.1",
    author='Guanliang Meng',
    author_email='mengguanliang@foxmail.com',
    description="To filter the sequences by translating the protein coding genes (PCGs) with proper genetic code table, if one of the PCGs has interal stop codon, filter out this sequence. See https://github.com/linzhi2013/breakSeqInNs_then_translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    url='https://github.com/linzhi2013/breakSeqInNs_then_translate',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['biopython>=1.54'],

    entry_points={
        'console_scripts': [
            'breakSeqInNs_then_translate=breakSeqInNs_then_translate.breakSeqInNs_then_translate:main',
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