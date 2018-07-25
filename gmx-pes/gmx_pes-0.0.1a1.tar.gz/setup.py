import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="gmx_pes",
    version="0.0.1a1",
    author="Elton Carvalho",
    author_email="elton.carvalho@ect.ufrn.br",
    description="A package to compare Potential Energy Surfaces in Gromacs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pessoal.ect.ufrn.br/~elton.carvalho",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry"
        ),
     install_requires=['pandas','panedr'],
     python_requires='>=3.5'
)
