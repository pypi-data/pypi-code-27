import setuptools
import MultiPoint

long_description = MultiPoint.__doc__

setuptools.setup(
    name="MultiPoint",
    version=MultiPoint.__version__,
    author="Quinn MacPherson",
    author_email="qmac@stanford.edu",
    description="WLC Structure Factor",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/qmacAstanford/MultiPointCalculation",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib', 'sympy', 'numba'],
    setup_requires=['sphinx', 'sphinx_rtd_theme'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ),
)
