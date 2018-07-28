from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='text2ml',
    version='2.0.1',
    packages=[''],
    url='https://github.com/marminino/text2ml',
    author='Alisson Lauffer',
    author_email='alissonvitortc@gmail.com',
    description='A module for Telegram Bot API that can format text + entities into formatted text',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
