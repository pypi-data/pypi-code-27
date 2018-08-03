from setuptools import find_packages, setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='tinyurls',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/rangertaha/tinyurl',
    license='MIT',
    install_requires=['tornado', 'SQLAlchemy', 'validators', 'fluent',
                      'pycodestyle', 'prometheus-client'],
    author='rangertaha',
    author_email='rangertaha@gmail.com',
    description='URL shortening service to be used in a microservices '
                'environment.',
    long_description=long_description,
    scripts=['bin/tinyurls'],
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'),
)
