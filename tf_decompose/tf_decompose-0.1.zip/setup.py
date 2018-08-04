from setuptools import setup, find_packages

setup(
    name='tf_decompose',
    version='0.1',
    author='ebigelow, chengscott',
    description='Tensor decomposition with TensorFlow',
    url='https://github.com/chengscott/tf-decompose',
    packages=find_packages(exclude=['examples', 'tests']),
    install_requires=[
        'tensorflow',
        'numpy',
        'scipy',
    ],
)
