from distutils.core import setup, Extension

addlib = Extension('addlib',
                    sources=['pyaddlib.c'])

setup(
    name='addlib',
    version='1.0',
    description='Address Library (CN)',
    ext_modules=[addlib]
    )
