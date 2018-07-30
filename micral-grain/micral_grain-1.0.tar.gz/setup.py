from setuptools import setup

def version():
	try:
		with open('version.txt') as f:
			return f.read()
	except:
		return "0.0.0"

def readme():
	try:
		with open('README.rst') as f:
			return f.read()
	except:
		return "Can't read README.rst"
		
setup(name='micral_grain',
      version=version(),
      description='Separation tool between coarse and ultrafine grain',
      long_description=readme(),
      author='Yann LEROY',
      author_email='yann.leroy102@orange.fr',
      license='MIT',
      packages=['micral_grain'],
	  install_requires=[
          'opencv-python',
          'numpy',
          'matplotlib',
		  'micral_grain_core'
      ],
	  include_package_data=True,
      zip_safe=False)