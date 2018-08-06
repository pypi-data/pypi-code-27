from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='necrophos-wsgi',
    version='0.0.1',
    description='wsgi-like server based on asyncio',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Elephant Liu',
    author_email='lexdene@gmail.com',
    url='https://github.com/lexdene/necrophos-wsgi',
    license='GPLv3',
    packages=['necrophos_wsgi'],
    entry_points={
        'console_scripts': [
            'necrophos_wsgi = necrophos_wsgi.main:main'
        ]
    },
)
