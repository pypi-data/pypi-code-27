from setuptools import setup

setup(name = 'prefepy',
	version='0.0.1',
	description='Prefence manager module to gather and show content to users',
	url='http://github.com/ballcarsen/',
	author='Carsen Ball',
	author_email='carsen@NEXTstory.com',
	license='Next Story Group, Carsen Ball',
	packages=['prefepy'],
	install_requires=['Flask-Cors','isodate', 'PyVimeo'],
	zip_safe=False)
