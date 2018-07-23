from setuptools import setup

__VERSION__ = '0.0.4'

setup(name='mlbootstrap',
      version=__VERSION__,
      description='A tiny bootstrap toolkit for deep learning',
      url='http://github.com/Luolc/MLBootstrap',
      author='Liangchen Luo',
      author_email='luolc.witty@gmail.com',
      license='MIT',
      packages=['mlbootstrap'],
      zip_safe=False,
      install_requires=[
          'PyYAML>=3.12',
          'fire==0.1.1'
      ])
