import setuptools

setuptools.setup(
    name='customdocs',
    version='0.1.0',
    packages=setuptools.find_packages(),
    author='Daniel Abercrombie',
    author_email='dabercro@mit.edu',
    description='Custom parsers for sphinx',
    url='https://github.com/dabercro/customdocs',
    install_requires=['sphinxcontrib-autoanysrc']
    )
