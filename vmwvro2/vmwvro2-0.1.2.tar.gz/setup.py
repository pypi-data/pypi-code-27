import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='vmwvro2',
      version='0.1.2',
      description='REST lib for VMWARE vRO',
      url='http://github.com/JoseIbanez/vmwvro2',
      author='Jose Ibanez',
      author_email='ibanez.j@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ],
      zip_safe=False)
