from setuptools import setup

setup(name='voice_robotifier',
        version='1.0',
        description='Turns your voice into text-to-speech!',
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
