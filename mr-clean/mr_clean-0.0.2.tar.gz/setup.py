from setuptools import setup,find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='mr_clean',
    version='0.0.2',
    author='A1Liu',
    author_email='albertymliu@gmail.com',
    description='A small package for cleaning data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/A1Liu/mr_clean',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent'
    ],
)
