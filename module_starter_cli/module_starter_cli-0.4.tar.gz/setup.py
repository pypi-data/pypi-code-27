from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


REQUIRED_MODULES = []
with open('requirements.txt') as file:
    REQUIRED_MODULES = [line.strip() for line in file]


setup(name='module_starter_cli',
      version='0.4',
      description='Starter project for deploying module',
      long_description=readme(),
      keywords='Module starter',
      url='http://github.com/storborg/funniest',
      author='Aumit Leon',
      author_email='aumitleon@gmail.com',
      license='MIT',
      packages=['module_scripts'],
      install_requires=REQUIRED_MODULES,
      entry_points={
          'console_scripts': ['module_starter=module_scripts.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)