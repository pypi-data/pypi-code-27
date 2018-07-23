from setuptools import setup

__VERSION__ = '0.0.4'

setup(name='mlbootstrap-tf',
      version=__VERSION__,
      description='A tiny bootstrap toolkit for deep learning with Tensorflow extionsions',
      url='http://github.com/Luolc/MLBootstrap-tf',
      author='Liangchen Luo',
      author_email='luolc.witty@gmail.com',
      license='MIT',
      packages=['mlbootstrap.tf'],
      zip_safe=False,
      install_requires=[
          'mlbootstrap=={}'.format(__VERSION__),
          'PyYAML>=3.12',
          'tensorflow>=1.8.0',
          'tqdm>=4.23.0'
      ])
