from setuptools import setup

setup(
    name='lemma_tokenizer',
    author='Patrick lee',
    author_email='lee.patrickmunseng@gmail.com',
    version="0.0.1",
    packages=['lemma_tokenizer'],
    description='lemma tokenizer class',
    platforms='Linux, MacOSX',
    install_requires=[
        'nltk',
        'pandas',
        'numpy'
    ],
    url='https://github.com/kcirtap2014/LemmaTokenizer',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
)
