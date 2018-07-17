from setuptools import setup

setup(
    name='instagram-analyzer',
    version='0.1.0',
    author='Nejc Korasa',
    author_email='nejc.korasa@gmail.com',
    description='Analyzes user\'s Instagram location geotags to find most frequent locations, countries, cities',
    url='https://github.com/nejckorasa/instagram-analyzer',
    download_url='https://github.com/nejckorasa/instagram-analyzer/archive/master.zip',
    packages=['instagram_analyzer'],
    license='Public domain',
    install_requires=[
        'beautifultable>=0.5.2',
        'requests>=2.19.1'
    ],
    keywords=['instagram', 'location', 'download', 'media', 'photos', 'videos', 'geocoding']
)
