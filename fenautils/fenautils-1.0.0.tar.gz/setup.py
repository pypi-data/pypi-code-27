from setuptools import setup

from fenautils import SEMANTIC_VERSION

"""
Resourses:
    https://pythonhosted.org/an_example_pypi_project/setuptools.html
    https://packaging.python.org/tutorials/packaging-projects/
    https://packaging.python.org/guides/distributing-packages-using-setuptools/

Examples:
    pylint: https://github.com/PyCQA/pylint/blob/master/setup.py
    pyexpander: https://bitbucket.org/goetzpf/pyexpander/src/b466de6fd801545650edfa790a18f022dc7e151a/setup.py?at=default&fileviewer=file-view-default

# update
python3 setup.py sdist bdist_wheel

# upload to testpypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload to regular pypi
twine upload dist/*

python3 -m pip install --user --index-url https://test.pypi.org/simple/ fena
python3 -m pip install --user fena
python3 -m pip install --user --upgrade fena
"""


setup(
    name="fenautils",
    version=SEMANTIC_VERSION,
    author="Austin Siew",
    author_email="glowing.locker@gmail.com",
    description=("Python utilities used alongside of the Fena preprocessor"),
    keywords="minecaft language fena preprocessor fenautils",
    url="https://github.com/Aquafina-water-bottle/fenautils",
    license='MIT',
    scripts=["fenautils.py"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)


