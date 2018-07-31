from setuptools import setup

setup(
	name='smartlog',
	version='0.1.0',
	description='Tools to log exceptions and better interface with logging library',
	url='https://github.com/dnut/smartlog',
	author='Drew Nutter',
	author_email='drew@drewnutter.com',
	license='GPLv3',
	package_dir={'': 'src'},
	packages=['smartlog'],
	zip_safe=False,
)