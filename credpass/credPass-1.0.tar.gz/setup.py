from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='credPass',
      version='1.0',
      description='python class to load credentials or other sensitive data',
      long_description=readme(),
      url='https://github.com/FedericoOlivieri/networkAutomation/',
      author='Federico Olivieri',
      author_email='lvrfrc87@gmail.com',
      license='MIT',
      packages=['credPass'],
      install_requires=['os', 'json'],
      zip_safe=False)
