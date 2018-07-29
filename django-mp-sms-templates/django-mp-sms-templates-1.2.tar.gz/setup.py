
from setuptools import setup, find_packages


version = '1.2'
url = 'https://github.com/pmaigutyak/mp-sms-templates'


setup(
    name='django-mp-sms-templates',
    version=version,
    description='SMS templates app',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT'
)
