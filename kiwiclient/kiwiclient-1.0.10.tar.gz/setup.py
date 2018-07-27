import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setuptools.setup(
      name='kiwiclient',
      version='1.0.10',
      author='ISC Clemenz und Weinbrecht GmbH',
      author_email='info@isc-kiwi.de',
      description='Client to the online version of ISC-Kiwi stability engine',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://www.isc-kiwi.de",
      license='Apache 2.0',
      packages=setuptools.find_packages(),
      install_requires=[
            'argparse',
            'xlrd',
            'xlsxwriter',
            'requests'
          ],
      platforms=['runs on any platform, best used together with MS-Excel'],
      keywords = ['excel', 'isc', 'kiwi', 'ki-wi', 'stability'],
      classifiers=(
        "Programming Language :: Python :: 3",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
      ),
      python_requires=">=3.4.0",
    )    