#-*- encoding: UTF-8 -*-
from setuptools import setup

setup(
    name = "tuStockSpider",          # 包名
    version = "0.15",              # 版本信息
    author="cansijyun",
    author_email="can_sijyun@yahoo.co.jp",
    description="China stock market everyday history data downloader",
    keywords="China stock market everyday history data downloader",
    long_description=open("README.rst").read(),
    #long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/cansijyun/StockHistorySpider",
    packages = ['tuStockSpider'],  # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    install_requires = [          # 安装依赖的其他包
    'lxml',
    'requests',
    ],
 )