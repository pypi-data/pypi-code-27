from setuptools import setup

setup(name='sharedql',
      version='0.1',
      description='Break graphene schema.py in multiples apps with single decorator',
      keywords='graphene apps plugins break schema.py multiples files',
      url='https://github.com/akaytatsu/sharedql',
      author='Thiago Freitad',
      author_email='thiagosistemas3@gmail.com',
      license='MIT',
      packages=['sharedql'],
      install_requires=[
          'graphene-django>=2.0',
      ],
      zip_safe=False)
