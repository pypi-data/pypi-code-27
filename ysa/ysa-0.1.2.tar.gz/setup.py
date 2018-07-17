import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ysa',
    version='0.1.2',
    author='shailyn ortiz(@M_abaader)',
    author_email='sortizjim@gmail.com',
    description='python client for the YSA api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sjortiz/YSA-PY',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests==2.19.1',
    ],
    test_dependencies=[
        'requests==2.19.1',
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ),
)
