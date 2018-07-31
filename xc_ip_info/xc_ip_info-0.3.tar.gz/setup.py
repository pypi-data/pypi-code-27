#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

print(find_packages())
setup(
    name='xc_ip_info',
    version=0.3,
	description='根据ip获取地址信息',
    long_description=open('README.rst').read(),
    author='liutianyi',
    author_email='liutianyi2014@xiaochuankeji.cn',
    maintainer='liutianyi',
    maintainer_email='liutianyi2014@xiaochuankeji.cn',
    license='BSD License',
	packages=find_packages(),
    platforms=["all"],
    url='http://git.izuiyou.com/liutianyi/ip_info',
    package_data={"xc_ip_info": ["data/17monipdb.dat"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['requests'],
)
