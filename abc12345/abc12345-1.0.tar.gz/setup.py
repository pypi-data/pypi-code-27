from distutils.core import setup
setup(
	name='abc12345',
	version='1.0',
	description='kmeans',
	url='',
	author='abhi',
	author_email='abhi@yahoo.com',
	license='MIT',
	py_modules=['demo'],
	packages=['myPackage'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',		
		],
	entry_points={
		'console_scripts': [
			'hello=mypackage.demo:demoprint',
			],
		}
	)