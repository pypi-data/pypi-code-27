from distutils.core import setup

setup(
    name='venkkat_math',
    version='1.0',
    description='A useful module',
    author='Man Foo',
    author_email='foomail@foo.com',
    packages=['venkkat_math'],
    py_modules=['Modules.modulo'],
    install_requires=['pandas==0.23.0']
)
