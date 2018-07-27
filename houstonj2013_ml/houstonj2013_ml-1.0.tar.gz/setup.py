from setuptools import setup
from setuptools.extension import Extension
try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True

ext_modules = []
if use_cython:
    ext_modules += cythonize('houstonj2013_ml/cyfun.pyx')
else:
    ext_modules += [Extension('houstonj2013_ml.cyfun',
                              ['houstonj2013_ml/cyfun.c'])]

setup(name='houstonj2013_ml',
      ext_modules=ext_modules,
      version='1.0',
      description='houstonj2013 machine learning modules',
      url='http://github.com/HoustonJ2013/HoustonJ2013_ml',
      author='Jingbo Liu',
      author_email='jingbo.liu2013@gmail.com',
      license='selfie',
      packages=['houstonj2013_ml'],
      zip_safe=False
      )

