from setuptools import setup

description = 'Analyzes user\'s Instagram location geotags to find most frequent locations, countries, cities'
dependencies = ['beautifultable>=0.5.2', 'requests>=2.19.1']

setup(
    name='instagram-analyzer',
    version='1.0.2',
    author='Nejc Korasa',
    author_email='nejc.korasa@gmail.com',
    description=description,
    url='https://github.com/nejckorasa/instagram-analyzer',
    download_url='https://github.com/nejckorasa/instagram-analyzer/archive/master.zip',
    packages=['instagram_analyzer'],
    license='Public domain',
    install_requires=dependencies,
    keywords=['instagram', 'location', 'download', 'media', 'photos', 'videos', 'geocoding']
)
