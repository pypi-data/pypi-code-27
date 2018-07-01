import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bold_identification",
    version="0.0.4",
    author='Guanliang Meng',
    author_email='mengguanliang@genomics.cn',
    description="To get taxa information of sequences from BOLD system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.4',
    url='http://mengguanliang.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['biopython==1.71', 'selenium==3.8.0', 
        'requests', 'pathlib'],

    entry_points={
        'console_scripts': [
            'bold_identification=bold_identification.BOLDv4_identification_selenium:main',
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