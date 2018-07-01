from setuptools import setup, find_packages


# python setup.py sdist upload -r pypi


setup(
    name='hsw2v',
    packages=find_packages(exclude=['tests']),
    version='1.0a3',
    description='Word2vec utility classes.',
    author='Tim Niven',
    author_email='tim.niven.public@gmail.com',
    url='https://github.com/timniven/w2v',
    download_url='https://github.com/timniven/w2v/archive/1.0a3.tar.gz',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='wor2vec nlp',
    install_requires=[
        'torch',
    ]
)
