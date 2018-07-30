#from distutils.core import setup
from setuptools import setup

setup(
	name='TICC',
	version='0.1.5.18',
	description='Solver for Toeplitz Inverse Covariance-based Clustering (TICC)',
	url='https://github.com/davidhallac/ticc',
	download_url='https://github.com/davidhallac/TICC/blob/blackbox/tarFile/TICC-0.1.5.18.tar.gz',
	install_requires=[
          'numpy', 'scipy', 'matplotlib', 'pandas', 
      ],
	packages=['ticc']
	)
