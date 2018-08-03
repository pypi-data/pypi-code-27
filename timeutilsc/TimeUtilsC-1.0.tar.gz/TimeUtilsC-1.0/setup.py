from distutils.core import setup, Extension

setup(name='TimeUtilsC', version='1.0',  \
      ext_modules=[Extension('TimeUtilsC', ['time-utils.c'])])
