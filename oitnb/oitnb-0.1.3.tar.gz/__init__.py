# coding: utf-8

_package_data = dict(
    full_package_name='oitnb',
    version_info=(0, 1, 3),
    __version__='0.1.3',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description="oitnb works around some of black's issues",
    keywords='automation formatter black pep8',
    entry_points=dict(console_scripts=['oitnb=oitnb.oitnb:main', 'omeld=oitnb.omeld:main']),
    license='MIT',
    since=2018,
    package_data={'_oitnb_lib2to3': ['*.txt']},
    python_requires='>=3.6',
    extra_packages=['_oitnb_lib2to3', '_oitnb_lib2to3.pgen2'],
    status='α',
    # universal=True,
    install_requires=['click>=6.5', 'attrs>=17.4.0', 'appdirs'],
    test_suite='_test.test_oitnb',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    tox=dict(env='py37,py36', fl8excl='_oitnb_lib2to3,_test,xtest'),
    oitnb=dict(double=True, line_length=88),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
