from setuptools import setup

setup(
    name='rgpubsub',
    version='0.0.3',
    packages=['rgpubsub','rgpubsub.clients'],
    author="Eirik Tenold",
    description="Simple helper utility to send Google Pubsub messages easily",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'google-cloud-pubsub'
    ],
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ),
)