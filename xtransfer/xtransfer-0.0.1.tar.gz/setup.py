"""
A file transfer cli to rule them all.
"""
import codecs
from setuptools import find_packages, setup

dependencies = [
    'click==6.7',
    'botocore==1.10.9',
    'boto3==1.7.9',
    'pysftp==0.2.9',
    'gnupg==2.3.1',
    'logging-gelf==0.0.9',
    'PyYAML==3.12'
]

setup(
    name='xtransfer',
    version='0.0.1',
    url='https://github.com/timbirk/python-xtransfer',
    license='BSD',
    author='Tim Birkett',
    author_email='tim.birkett@itv.com',
    description='A file transfer cli to rule them all.',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'xtransfer = xtransfer.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
