import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmpk",
    version="1.0.0",
    author="leoetlino",
    author_email="leo@leolam.fr",
    description="Library and tool for Nintendo's TMPK archive format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leoetlino/tmpk",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': [
            'tmpk = tmpk.__main__:main',
            'tmpktool = tmpk.__main__:main',
        ]
    },
)
