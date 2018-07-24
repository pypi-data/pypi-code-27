from setuptools import setup
from pathlib import Path
import os

file_path = Path(os.path.dirname(os.path.abspath(__file__)))
with open(file_path/"README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='itunes2Spotify',
    version='0.1.0',
    description='Transfer albums from iTunes to Spotify',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/colbymorrison/itunes2spotify',
    author='Colby Morrison',
    author_email='colbyamorrison@gmail.com',
    license='MIT',
    install_requires=[
        'spotipy', 'click'
    ],
    packages=['itunes2Spotify'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'i2s = itunes2spotify.itunes2spotify:main'
        ]
    })
