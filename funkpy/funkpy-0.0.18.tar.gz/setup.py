from setuptools import setup
from funkpy import __version__, __name__
setup(
  name=__name__,
  version=__version__,
  packages=[__name__],
  author="vnl2k",
  license='MIT',
  url="https://github.com/vnl2k/funkpy",
  python_requires='>=3.5'
)
