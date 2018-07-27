import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ['tweepy>=3']

setuptools.setup(
    name='stream-tweets',
    version='1.0.1',
    author='Wesley Uykimpang',
    author_email='wesu07@gmail.com',
    description='stream tweets to a queue',
    long_description='stream tweets to a queue for a finite amount of time \
        that can be parallelized with a consumption process',
    url='https://github.com/wesuuu/queue_tweets',
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    )
)
