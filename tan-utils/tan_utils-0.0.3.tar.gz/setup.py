import setuptools

setuptools.setup(
  name='tan_utils',
  version='0.0.3',
  description='Tan\'s utilities',
  url='https://github.com/tannn1995/tan_utils',
  author='Tan Nguyen',
  author_email='tan.nguyen.tn@hotmail.com',
  packages=setuptools.find_packages(),
  classifiers=(
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ),
  entry_points = {
   'console_scripts': ['tan-utils=tan_utils.tan_utils_cli:main'],
  }
)
