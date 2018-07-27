from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "cyfun",
    ext_modules=cythonize("cyfun.pyx")
)