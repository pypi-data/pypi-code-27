from setuptools import setup, find_packages
 
setup(name='python_ytg',
      version='0.0.1',
      url='https://gitlab.com/databulle/python_ytg',
      license='MIT',
      author='Julien Deneuville',
      author_email='julien@databulle.com',
      description='Easily use YourTextGuru API in Python.',
      keywords='seo yourtextguru api google content optimization nlp',
      packages=find_packages(exclude=['tests']),
      install_requires=['requests'],
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      zip_safe=False,
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
      )
    )