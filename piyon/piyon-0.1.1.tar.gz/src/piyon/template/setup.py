from setuptools import setup, find_packages

VERSION = '0.1.1'

setup(
    name='$PROJECT_NAME$',
    description='create a python project with pytest and pytest plugins',

    version=VERSION,

    author='kiyon',
    email='kiyonlin@gmail.com',
    url='https://github.com/kiyonlin/piyon',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=[
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
        'pytest-flakes',
    ],
)
