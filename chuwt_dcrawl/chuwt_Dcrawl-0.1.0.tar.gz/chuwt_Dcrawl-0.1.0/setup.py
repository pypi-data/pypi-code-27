from setuptools import setup, find_packages

setup(
    name='chuwt_Dcrawl',
    version='0.1.0',
    description=(
        '一个分布式异步爬虫'
    ),
    long_description=open('README.md').read(),
    author='chuwt',
    author_email='weitaochu@gmail.com',
    maintainer='chuwt',
    maintainer_email='weitaochu@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/chuwt/Dcrawl',
    install_requires=[
        'redis',
        'aiohttp'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)