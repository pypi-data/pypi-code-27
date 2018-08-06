from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyxel-catpointer',
    description='Silly game powered by pyxel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.6',
    author='Santos Gallegos',
    author_email='santos_g@outlook.com',
    license='MIT',
    url='https://github.com/stsewd/cat-pointer-game',
    packages=find_packages(),
    package_data={
        '': ['assets/*'],
    },
    install_requires=['pyxel<1'],
    entry_points={
        'console_scripts': [
            'catpointer = catpointer.game:App',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Topic :: Games/Entertainment :: Arcade',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
