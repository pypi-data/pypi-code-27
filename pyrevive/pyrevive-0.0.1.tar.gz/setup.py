from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyrevive',
    version='0.0.1',
    description='Revive Hardware Restarter API Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RevolutionRigs/pyrevive',
    author='Revolution Rigs',
    author_email='nathan@revolutionrigs.com',
    license='GNU v3.0',
    packages=['pyrevive'],
    install_requires=[ 'requests' ],
    zip_safe=False)
