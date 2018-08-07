from setuptools import setup, find_packages
pkg = "etreetools"
ver = '0.1.2'
setup(
    name             = pkg,
    version          = ver,
    description      = "ElementTree utilities",
    author           = "jikan@cock.li",
    author_email     = "jikan@cock.li",
    license          = "LGPLv3",
    url              = "https://hydra.ecd.space/jikan/etreetools/",
    packages         = find_packages(),
    install_requires = [],
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])
