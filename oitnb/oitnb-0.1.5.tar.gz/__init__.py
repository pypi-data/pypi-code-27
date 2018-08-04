# coding: utf-8

_package_data = dict(
    full_package_name=u"oitnb",
    version_info=(0, 1, 5),
    __version__="0.1.5",
    author=u"Anthon van der Neut",
    author_email=u"a.van.der.neut@ruamel.eu",
    description=u"oitnb works around some of black's issues",
    keywords=u"automation formatter black pep8",
    entry_points=dict(
        console_scripts=[u"oitnb=oitnb.oitnb:main", u"omeld=oitnb.omeld:main"]
    ),
    license=u"MIT",
    since=2018,
    package_data={u"_oitnb_lib2to3": [u"*.txt"]},
    python_requires=u">=3.6",
    extra_packages=[u"_oitnb_lib2to3", u"_oitnb_lib2to3.pgen2"],
    status=u"α",
    # universal=True,
    install_requires=[u"click>=6.5", u"attrs>=17.4.0", u"appdirs"],
    test_suite=u"_test.test_oitnb",
    classifiers=[
        u"Environment :: Console",
        u"Operating System :: OS Independent",
        u"Programming Language :: Python",
        u"Programming Language :: Python :: 3.6",
        u"Programming Language :: Python :: 3.7",
        u"Programming Language :: Python :: 3 :: Only",
        u"Topic :: Software Development :: Libraries :: Python Modules",
        u"Topic :: Software Development :: Quality Assurance",
    ],
    # tox=dict(env=u"py37,py36", fl8excl=u"_oitnb_lib2to3,_test,xtest"),
    oitnb=dict(double=True, line_length=88),
)


version_info = _package_data["version_info"]
__version__ = _package_data["__version__"]
