from setuptools import setup, find_packages

setup(name='hwaves',
    version='0.0.1',
    url='https://github.com/lensonp/hwaves.git',
    description='Compute and plot hydrogenic wavefunctions',
    author='Lenson A. Pellouchoud',
    license='BSD',
    author_email='',
    install_requires=['numpy','scipy','masstable','periodictable'],
    packages=find_packages(),
    package_data={}
)


