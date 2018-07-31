from setuptools import setup, find_packages


setup(name='tru',
      version='0.0.3',
      description='https://github.com/TroyRetter/TRU',
      long_description="""
Wraps some standard python commands for brevity. Parameters default to the canonical data science use case (or the author's primary use case)

see: https://github.com/TroyRetter/TRU
""",
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
