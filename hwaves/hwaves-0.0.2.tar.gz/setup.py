from setuptools import setup, find_packages

longdesc = 'Current capabilities: '\
    '\n - Compute and plot radial wavefunctions for any n, l'\
    '\n - Compute and plot spherical harmonics for any l, m'\
    '\n - Compute real-space density of hydrogenic eigenfunctions for any n, m, l'\
    '\n - Compute real-space density of real-valued wavefunctions (1s, 2p, 3dx2-y2, etc.)'\
    '\n - Plot (and provide polygon data) for real-space density isosurfaces of any value'

setup(name='hwaves',
    version='0.0.2',
    url='https://github.com/lensonp/hwaves.git',
    description='Compute and plot hydrogenic wavefunctions',
    long_description=longdesc,
    author='Lenson A. Pellouchoud',
    license='BSD',
    author_email='',
    install_requires=['numpy','scipy','masstable','periodictable'],
    packages=find_packages(),
    package_data={}
)


