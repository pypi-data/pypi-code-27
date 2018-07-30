from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='chp',
    version='0.0.1',
    description='Composable HTML in Python',
    author='Thomas Binetruy',
    author_email='tbinetruy@gmail.com',
    url='https://github.com/tbinetruy/CHIP',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.org'),
    license='MIT',
    keywords='html',
    tests_require=['tox'],
    extras_require=dict(
        dev=[
          'django>=2.1rc1',
        ],
        test=[
            'pytest',
            'pytest-django',
            'pytest-mock',
            'mock',
        ],
    ),
    entry_points={
        'console_scripts': [
            'chp-django = chp.django.example.manage:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
