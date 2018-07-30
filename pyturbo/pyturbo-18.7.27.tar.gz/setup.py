from setuptools import setup, find_packages

setup(
    name='pyturbo',
    version='18.7.27',
    description=(
        'This project contains a variety of different python packages'
    ),
    author='aikudexiaohai',
    author_email='1052220704@qq.com',

    maintainer='aikudexiaohai',
    maintainer_email='1052220704@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=['all'],
    url='https://github.com/aikudexiaohai/pyturbo',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'tensorflow',
        'opencv-python',
        'numpy',
        'six'
    ]
)