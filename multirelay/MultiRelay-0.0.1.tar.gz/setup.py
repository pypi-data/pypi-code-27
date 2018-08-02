import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                    = "MultiRelay",
    version                 = "0.0.1",
    author                  = "Chiang Iheng",
    author_email            = "jj11hh@live.com",
    description             = "A simple TCP/UDP relay for multiple connection",
    long_description        = long_description,
    long_description_content_type
                            = "text/markdown",
    url                     = "https://github.com/jj11hh/MultiRelay",
    packages                = setuptools.find_packages(),
    classifiers             = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Topic :: System :: Networking",
        "Development Status :: 1 - Planning",
    ),
)

