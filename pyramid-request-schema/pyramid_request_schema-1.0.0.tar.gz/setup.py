from setuptools import setup

setup(
    name='pyramid_request_schema',
    version='1.0.0',
    packages=['pyramid_request_schema'],
    install_requires=[
        "colander",
        "pyramid",
    ],
    url='https://github.com/sighalt/pyramid_request_schema',
    license='MIT',
    author='Jakob Rößler',
    author_email='roessler@sighalt.de',
    description='Pyramid extension for validating incoming requests'
)
