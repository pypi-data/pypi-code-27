from setuptools import setup

setup(name='oxyba',
      version='0.13.0',
      description='my wrapper functions and classes for python',
      url='http://github.com/ulf1/oxyba',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['oxyba'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'urllib3', 'setuptools', 'datetime', 'nose'],
      python_requires='>=3',
      zip_safe=False)

