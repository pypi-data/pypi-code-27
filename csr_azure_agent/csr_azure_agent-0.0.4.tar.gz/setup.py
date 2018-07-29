from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print "We are running in the postInstallCommand"
        cwd = os.path.dirname(os.path.realpath(__file__))
        check_call("bash %s/csr_waagent_install.sh" % cwd, shell=True)
        install.run(self)


project_name = 'csr_azure_agent'
project_ver = '0.0.4'
setup(
    name=project_name,
    version=project_ver,
    description='A library to install Azure Waagent on CSR',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'azure', 'csr1000v', 'csr', 'guestshell'],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    },
)
