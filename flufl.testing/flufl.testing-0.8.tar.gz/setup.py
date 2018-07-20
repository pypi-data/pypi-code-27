from setup_helpers import get_version, require_python
from setuptools import setup, find_packages


require_python(0x030400f0)
__version__ = get_version('flufl/testing/__init__.py')


setup(
    name='flufl.testing',
    version=__version__,
    namespace_packages=['flufl'],
    packages=find_packages(),
    include_package_data=True,
    maintainer='Barry Warsaw',
    maintainer_email='barry@python.org',
    description='A small collection of test tool plugins',
    license='ASLv2',
    url='https://gitlab.com/warsaw/flufl.testing',
    download_url='https://pypi.python.org/pypi/flufl.testing',
    entry_points={
        'flake8.extension': ['U4 = flufl.testing.imports:ImportOrder'],
        },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        ]
    )
