import setuptools
import cx_Freeze
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.1.1'
short_description = 'A recreation of the door puzzles from the Nonary game, 999.'

setuptools.setup(
    name='numbereddoor-game',
    version=version,
    author='Coul Greer',
    author_email='coulgreer1@hotmail.com',
    description=short_description,
    long_description=long_description,
    url='https://github.com/cagreer18/NumberedDoorGame',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ]
)

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

cx_Freeze.setup(
    name='numbereddoor-game',
    options={"build_exe": {
        'include_files': ['images']
    }},
    version=version,
    description=short_description,
    executables=[cx_Freeze.Executable('main_game.py', base=base)]
)
