from setuptools import setup

NAME='mscan'

setup(
    name=NAME,
    description="Looking for a job description on the website monster.com.",
    long_description=open("README.md").read(),
    url="https://github.com/sm-svyat/monsterscan",
    version='0.0.1',
    packages=[NAME],
)
