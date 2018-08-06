from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='bc_dock_util',
    version='0.0.9',
    author='caifh',
    author_email='caifh@tianxiaxinyong.com',
    description='B client docking tianxiaxinyong service sdk util.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/pytxxy/bc_dock_util',
    install_requires=[
        'pycryptodome>=3.5.1',
        'cryptography>=2.3',
        'Requests>=2.19.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
