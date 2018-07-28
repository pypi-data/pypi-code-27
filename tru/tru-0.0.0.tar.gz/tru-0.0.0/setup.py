from setuptools import setup, find_packages


setup(name='tru',
      version='0.0.0',
      description='',
      long_description="",
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      entry_points={
          "console_scripts": [
          ]
      },
      keywords='',
      url='',
      author='Troy Retter',
      author_email='troyretter@gmail.com',
      license='',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'pandas', 'PyYAML',],
      zip_safe=False)
