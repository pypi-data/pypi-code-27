from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cone',
      version='0.0.0',
      description=readme(),
      #url='http://github.com/storborg/funniest',
      author='Olivier Trepanier',
      author_email='olitrepanier@hotmail.com',
      packages=['cone'],
      install_requires=[
          'Flask',
          'requests'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['cone = cone.__main__:main']},
      zip_safe=False)