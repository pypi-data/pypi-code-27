import setuptools

requirements_file = [line.strip() for line in open('requirements.txt').readlines()
                     if line.strip() and not line.startswith('#')]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Data-Access-Layer',
    version='1.0',
    packages=setuptools.find_packages(),
    url='https://github.com/iurdaniz7/Data-Access-Layer',
    license='MIT',
    author='Ion Urdaniz',
    author_email='i.urdaniz7@gmail.com',
    long_description=long_description,
    description='Tool for interacting with databases',
    install_requires=requirements_file,
    scripts=['bin/Manexercise.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    test_suite='tests'
)
