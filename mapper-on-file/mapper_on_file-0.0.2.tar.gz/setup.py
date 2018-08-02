from setuptools import setup

setup(name='mapper_on_file',
      version='0.0.2',
      description='This is a mapper based on deep_mapper1. It will help you convert object from one to other based on configuration.',
      url='https://github.com/cao5zy/mapper_on_file',
      author='zongying.cao',
      author_email='zongying_cao@163.com',
      license='MIT',
      packages=['mapper_on_file'],
      install_requires=["deep_mapper1>=0.0.1"],
      zip_safe=False)
