from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='s3-to-disk',
    version='0.1.1',
    author='Hassene Ben Salem',
    author_email='bensalemhsn@gmail.com',
    description='A simple tool to synchronizes S3 to a local folder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kardaj/s3-to-disk',
    install_requires=['future', 'boto3', 'awscli'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            's3-to-disk=s3_to_disk:main'
        ]
    },
    classifiers=(
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),

)
