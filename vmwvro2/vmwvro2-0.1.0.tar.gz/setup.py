from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='vmwvro2',
      version='0.1.0',
      description='REST lib for VMWARE vRO',
      url='http://github.com/JoseIbanez/vmwvro2',
      author='Jose Ibanez',
      author_email='ibanez.j@gmail.com',
      license='MIT',
      packages=['vmwvro2'],
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ],
      zip_safe=False)