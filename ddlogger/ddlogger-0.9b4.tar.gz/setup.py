import setuptools

with open('README.md') as infile:
    long_description = infile.read()

setuptools.setup(
    name='ddlogger',
    version='0.9b4',
    author='Kaiwen Wu',
    author_email='kps6326@hotmail.com',
    description='Logs progress by printing dots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kkew3/dot-dot-logger',
    packages=setuptools.find_packages(),
    install_requires=[
        'future',
    ],
    classifiers=(
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
