import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='classRant',
    version='1.0',
    description='A simpler class-based interface to devRantSimple',
    url='https://github.com/Ewpratten/classRaant',
    author='Evan Pratten',
    author_email='ewpratten@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['devRantSimple'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ),
)
