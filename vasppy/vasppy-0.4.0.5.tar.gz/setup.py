"""
vasppy: utilities for working with VASP input and output
"""

from setuptools import setup, find_packages
from vasppy import __version__ as VERSION

scripts = [ 'murnfit', 
            'vasp_summary', 
            'poscar_to_cif', 
            'potcar_spec',
            'effective_mass',
            'fat_bands',
            'pimaim_to_poscar',
            'pimaim_to_xtl',
            'poscar_sort',
            'poscar_to_pimaim',
            'poscar_to_xtl',
            'proc_poscar',
            'rotate_poscar',
            'spacegroup',
            'vasp_grid',
            'xdatcar_to_disp',
            'xdatcar_to_rdf' ]

setup(
    name='vasppy',
    version=VERSION,
    description='Utilities for working with VASP input and output',
    long_description=open( 'README.md' ).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bjmorgan/vasppy', 
    author='Benjamin J. Morgan',
    author_email='b.j.morgan@bath.ac.uk',
    license='MIT',
    packages=find_packages( exclude=[ 'docs', 'tests*' ] ),
    download_url='https://github.com/bjmorgan/vasppy/archive/{}.tar.gz'.format( VERSION ),
    keywords=[ 'vasp' ],
    package_data={ 'vasppy': ['data/*.yaml'] },
    entry_points={ 'console_scripts': [
                       '{} = vasppy.scripts.{}:main'.format( s, s ) for s in scripts ] },
    install_requires=[ 'numpy',
                       'pandas',
                       'pymatgen',
                       'PyYAML', 
                       'coverage==4.3.4',
                       'codeclimate-test-reporter' ]
    )
