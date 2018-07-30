from setuptools import setup

setup(
    name='security_group_auditor',
    install_requires=["boto3",
                      "pandas"],
    version='0.1',
    packages=[''],
    url='https://github.com/vmanikes/AWS_security_group_auditor',
    license='',
    author='Venkata S S K M Chaitanya',
    author_email='kchaitanya39@gmail.com',
    description='A Python security group auditor that will scan all your AWS regions and will return the security group rules in a CSV file to easily audit '
)
