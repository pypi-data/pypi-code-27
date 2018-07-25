from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cone',
      version='0.0.1',
      description='A tool to sync projects to Roblox Studio',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://gitlab.com/rbx-cone/cone',
      author='Olivier Trepanier',
      author_email='olitrepanier@hotmail.com',
      keywords='roblox',
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