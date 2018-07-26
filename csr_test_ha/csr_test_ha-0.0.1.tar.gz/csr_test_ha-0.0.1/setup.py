from distutils.core import setup
project_name = 'csr_test_ha'
project_ver = '0.0.1'
setup(
    name=project_name,
    version=project_ver,
    description='A Test package for testing HA on Azure',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    scripts=["bin/as_aws_cli.py"],
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/csr_test_ha',
    download_url='https://github4-chn.cisco.com/csr1000v-azure/csr_test_ha',
    keywords=['cisco', 'azure', 'ha', 'high availability'],
    classifiers=[],
    license="MIT",
    install_requires=[
        'csr_azure_utils',
        'csr_ha'
    ],
)
