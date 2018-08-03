# -*- encoding: utf-8

from setuptools import find_packages, setup

import os


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')
README = local_file('README.md')


with open(local_file('src/platformcli/version.py')) as o:
    exec(o.read())

assert __version__ is not None


if __name__ == '__main__':
    setup(
        name='wellcome-platform-cli',
        version=__version__,
        description='Build tooling for the Wellcome Digital Platform',
        long_description=open(README).read(),
        packages=find_packages(SOURCE),
        package_dir={'': SOURCE},
        install_requires=[
            'click>=6.7,<7',
        ],
        entry_points='''
            [console_scripts]
            platform=platformcli.cli:cli
        ''',
        url='http://github.com/wellcometrust/platform-cli',
        author='Wellcome Digital Platform',
        author_email='wellcomedigitalplatform@wellcome.ac.uk',
        license='License :: OSI Approved :: MIT License',
    )
