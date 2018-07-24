from setuptools import setup
import atuin

setup(
    name='atuin',
    version=atuin.__version__,
    description='''A tool for challenge creation and management
                    for CSTEM/Roboplay Competition''',
    author='Steven Herman',
    author_email='stejher@gmail.com',
    license='GPL3',
    packages=['atuin'],
    install_requires=[
        'colorama',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'atuin = atuin.__main__:main'
        ]
    })
