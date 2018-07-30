import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='robin8_utils',
    version='0.0.2',
    author='Robin8',
    author_email='vvasyuk@robin8.com',
    description='Utils used in Robin8 projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Robin8Put/pmes/tree/master/utils',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ),
)