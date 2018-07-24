from setuptools import setup

setup(
    name='revfyawo.mongo',
    version='0.0.6',
    description='A mongo ODM',
    url='https://github.com/revfyawo/revfyawo-mongo',
    author='Lucien Haurat',
    author_email='lucien.haurat@gmail.com',
    packages=['revfyawo.mongo'],
    install_requires=['pymongo~=3.7'],
)

