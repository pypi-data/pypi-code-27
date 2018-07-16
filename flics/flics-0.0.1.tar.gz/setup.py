import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flics",
    version="0.0.1",
    author="Zvi Baratz",
    author_email="z.baratz@gmail.com",
    description=
    "Reimplementation of the flow image correlation spectroscopy (FLICS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZviBaratz/flics",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='spectroscopy analysis blood flow microcirculation velocity',
    install_requires=['numpy', 'scipy', 'pillow'],
    extras_require={
        'dev': ['flake8', 'yapf'],
        'test': ['pytest']
    },
    project_urls={
        'Original Article':
        'https://www.nature.com/articles/srep07341',
        'Data from Article':
        'https://www.dropbox.com/s/y1o652z1djpcjz6/f03_x5_4p36fps-Ch1.tif?dl=0',
        'GUI Package':
        'https://github.com/PBLab/flics/',
        'Bug Reports':
        'https://github.com/ZviBaratz/flics/issues',
        'Source':
        'https://github.com/ZviBaratz/flics/',
    },
)
