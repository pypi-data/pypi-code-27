from setuptools import setup  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='libra_py_001_07',
    version='0.0.1',
    description='Split Linearized Bregman Iteration',
    long_description=long_description,
    url='https://github.com/tansey/smoothfdr',
    author='Xinwei Sun',
    author_email='sxwxiaoxiaohehe@pku.edu.cn',
    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='sparsity regularization path Lasso variable-selection',

    packages=['libra_py_001_07'],
    package_dir={'libra_py_001_07': 'libra_py_001_07'},
    install_requires=[
              'numpy',
              'scipy', 
              'matplotlib', 
              'scikit-learn'],
   
)
