from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='voice_robotifier',
        version='1.0.3',
        description='Turns your voice into text-to-speech!',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Reid Huntley',
        author_email='reidbhuntley@gmail.com',
        url='https://github.com/reidbhuntley/voice_robotifier',
        license='MIT',
        packages=['voice_robotifier'],
        install_requires=[
            'SpeechRecognition>=3.8.1',
            'keyboard>=0.13.2',
            'PyAudio>=0.2.11',
            'comtypes'
        ],
        zip_safe=False)
