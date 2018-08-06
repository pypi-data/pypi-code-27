from setuptools import setup
from setuptools import find_packages

lineiter = (line.strip() for line in open('requirements/base.txt'))
required = [line for line in lineiter if line and not line.startswith("#")]
required = list(map(lambda x: x.split(' ')[0], required))


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='lettuce_rest',
    version='1.0.1',
    author='Victor Cabello',
    author_email='vmeca87@gmail.com',
    url='https://gitlab.com/vmeca87/lettuce_rest',
    description="BDD-style Rest API testing tool",
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    package_data={},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=required,
)
