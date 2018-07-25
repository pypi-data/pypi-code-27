import os
import re
from setuptools import setup
from setuptools import find_packages


app_name='hxlti'
project_name='{}-djapp'.format(app_name)

def get_version(*file_paths):
    """Retrieves the version from [your_package]/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version(app_name, "__init__.py")


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Django',
    'django-model-utils',
    'pytz',
    'lti',
    'oauthlib',
    'redis',
]

test_requirements = [
    'mock',
    'tox',
    'pytest',
    'pytest-runner',
]

setup(
    name=project_name,
    version=version,
    description="hx django lti provider for edx",
    long_description=readme,
    author="nmaekawa",
    author_email='nmaekawa@g.harvard.edu',
    url='https://github.com/nmaekawa/' + project_name,
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='hx lti provider ' + project_name,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
