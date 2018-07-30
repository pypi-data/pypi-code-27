from setuptools import setup

setup(
    author='Radomír Bosák',
    author_email='radomir.bosak@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Python Module for Interacting with Anime Planet',
    entry_points={
        'console_scripts': [
            'animeplanet = animeplanet.animeplanet:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'requests_html'
    ],
    keywords=['animeplanet', 'anime', 'cli'],
    license='MIT',
    name='animeplanet',
    packages=['animeplanet'],
    url='https://github.com/radomirbosak/animeplanet',
    version='0.1.0',
)
