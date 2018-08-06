from setuptools import setup, find_packages

setup(
    name="Vipc",
    packages=find_packages(),
    version='0.0.4',
    description="command line tool for auto tuner",
    author="liyang",
    author_email='liyang@vipcode.com',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    url='https://github.com/ly1016799291/ceshi.git',
    install_requires=[
        'baidu-aip',
        'pyaudio',
        'soundfile',
        'pygame',
    ]
)