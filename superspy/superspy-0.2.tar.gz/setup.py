from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='superspy',
    version='0.2',
    description='Small Uncomplicated Plugin Extensible Reliable Shell in PYthon',
    long_description=long_description,
    url='https://github.com/Kamik423/superspy',
    author='Hans',
    author_email='contact.kamik423@gmail.com',
    license='MIT',
    packages=['superspy'],
    zip_safe=False,
    install_requires=['pluginbase'],
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
