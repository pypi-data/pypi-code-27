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

setup(name='micral_harmonic_core',
      version=version(),
      description='Measurement tools of the harmonicity of the microstructure - core module',
      long_description=readme(),
      author='Yann LEROY',
      author_email='yann.leroy102@orange.fr',
      license='MIT',
      packages=['micral_harmonic_core'],
	  install_requires=[
          'opencv-python',
          'numpy',
		  'micral_utils'
      ],
	  include_package_data=True,
      zip_safe=False)