from setuptools import setup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name="ety-tools",
    packages=['ety-tools'],
    version='0.0.2',
    description="some python toolkits",
    author="ety",
    author_email='ety@etyhk.com',
    url="http://etyhk.com",
    # download_url='https://github.com/username/reponame/archive/0.1.tar.gz',
    # keywords=['command', 'line', 'tool'],
    classifiers=[],
)