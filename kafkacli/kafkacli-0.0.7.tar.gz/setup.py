from setuptools import setup
from kafkacli import util

setup(
    name = 'kafkacli',
    version = util.VERSION,
    description = 'Apache Kafka CLI utility tool.',
    author = 'Ryan Yuan',
    author_email = 'ryan.yuan@outlook.com',
    url = 'https://github.com/ryanyuan/kafkacli',
    packages = ['kafkacli'],
    install_requires=[
        'kafka'
    ],
    entry_points = {
        'console_scripts': [
            'kafkacli = kafkacli.__main__:main'
        ]
    }
)