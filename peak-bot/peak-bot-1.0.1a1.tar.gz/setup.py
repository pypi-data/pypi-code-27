from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='peak-bot',
    version='1.0.1a1', 
    description='Lightweight, simple, speech-to-text-oriented bot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/doriclazar/peak_bot',
    author='Lazar Doric',
    author_email='doriclazar@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Home Automation',
        'Topic :: Office/Business',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='peak bots',
    packages=find_packages(),
    install_requires=['pyaudio', 'google-cloud-speech'],
    package_data={'peak_data': ['*.json',],},
    include_package_data=True,
    data_files=[
        ('peak_data', ['peak_bot/peak_data/library/core.json', 'peak_bot/peak_data/library/core/append_to_file.json', 'peak_bot/peak_data/library/core/write_to_file.json', 'peak_bot/peak_data/library/networking.json', 'peak_bot/peak_data/library/networking/ping.json', 'peak_bot/peak_data/library/file_system.json', 'peak_bot/peak_data/library/file_system/copy.json', 'peak_bot/peak_data/configuration/settings.json', 'peak_bot/peak_data/configuration/audio_base.json', 'peak_bot/peak_data/configuration/lang_base.json']),
    ],
    entry_points = {
        "console_scripts": ['peak-bot=peak_bot.__main__:main']
        },
    project_urls={
        'Bug Reports': 'https://github.com/doriclazar/peak_bot/issues',
        'Source': 'https://github.com/doriclazar/peak_bot/',
    },
)
