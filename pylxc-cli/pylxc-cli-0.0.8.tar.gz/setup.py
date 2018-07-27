"""Setup app from setup.cfg"""
from setuptools import find_packages, setup

__version__ = '0.0.8'


with open('requirements.txt', 'r') as fh:
    reqs = fh.read()

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='pylxc-cli',
    version=__version__,
    include_package_data=True,
    packages=find_packages(),
    author='pylxc',
    author_email='vnaraujo@ciandt.com',
    entry_points={
        'console_scripts': [
            'pylxc_cli=pylxc.__main__:cli'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=reqs,
    description='LXC client',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    python_requires='>=3',
)
