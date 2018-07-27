
from setuptools import setup, find_packages


version = '1.0'
url = 'https://github.com/pmaigutyak/mp-shop-wishlist'


setup(
    name='django-mp-shop-wishlist',
    version=version,
    description='Django shop wishlist apps',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT'
)
