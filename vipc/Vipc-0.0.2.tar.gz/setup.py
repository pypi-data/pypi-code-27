from setuptools import setup, find_packages

setup(
    name="Vipc",
    packages=find_packages(),
    version='0.0.2',
    description="command line tool for auto tuner",
    author="liyang",
    author_email='liyang@vipcode.com',
    
    url='https://github.com/ly1016799291/ceshi.git',
    install_requires=[
        'baidu-aip',
        'pyaudio',
        'soundfile',
        'pygame',
    ]
)