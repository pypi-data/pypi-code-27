import pathlib
from setuptools import setup, find_packages


setup(
    name="distinfo",
    version="0.1.0",
    author="Arthur Noel",
    author_email="arthur@0compute.net",
    description="Extract metadata from Python source distributions",
    long_description=open(pathlib.Path(__file__).parent / "README.md").read(),
    long_description_content_type="text/markdown",
    keywords=("packaging"),
    license="GPL-3.0-or-later",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        'Operating System :: POSIX',
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Archiving :: Packaging",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points=dict(
        console_scripts=(
            "distinfo = distinfo.cli:main",
        ),
    ),
    setup_requires=(
        "pytest-runner",
    ),
    install_requires=(
        "appdirs",
        "click",
        "coloredlogs",
        "munch",
        "pip",
        "pipreqs",
        "property-manager",
        "ptpython",
        "requirementslib",
        "setuptools",
        "tox",
        "wrapt",
        "pyyaml",
    ),
    # FIXME: nixipy misses this
    tests_require=(
        "pytest",
    ),
    extras_require=dict(
        dev=(
            "pdbpp",
            # "prospector[with_everything]",
            "pycmd",
            "pytest-cov",
            "pytest-sugar",
            "twine",
        ),
    ),
)
