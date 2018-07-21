from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='s3-to-disk',
    version='0.1.0',
    author='Hassene Ben Salem',
    author_email='bensalemhsn@gmail.com',
    description='A simple tool to synchronizes S3 to a local folder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['future', 'boto3', 'awscli'],
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
