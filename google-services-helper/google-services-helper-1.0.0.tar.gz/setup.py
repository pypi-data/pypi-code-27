from setuptools import setup

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = ''

setup(
    name='google-services-helper',
    version='1.0.0',
    packages=['vedavaapi', 'vedavaapi.google_helper', 'vedavaapi.google_helper.oauth', 'vedavaapi.google_helper.gdrive',
              'vedavaapi.google_helper.gsheets'],
    url='https://github.com/vedavaapi',
    author='vedavaapi',
    author_email='vvsvmb151@gmail.com',
    description='google api helper for vedavaapi project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['flask', 'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2', 'google-api-python-client'],
    classifiers=(
            "Programming Language :: Python :: 2.7",
            "Operating System :: OS Independent",
    )
)
