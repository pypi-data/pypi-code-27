from setuptools import setup

def version():
	try:
		with open('version.txt') as f:
			return f.read()
	except:
		return "0.0.0"
	
setup(name='micral_utils',
      version=version(),
      description='Utilities for Micral packages',
      author='Yann LEROY',
      author_email='yann.leroy102@orange.fr',
      license='MIT',
      packages=['micral_utils'],
	  install_requires=[
          'numpy'
      ],
	  include_package_data=True,
      zip_safe=False)