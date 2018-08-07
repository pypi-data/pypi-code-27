from distutils.core import setup

from setuptools import setup, find_packages

setup(

    name = 'test_vipman_model',

    version = '0.0.1',

    keywords = ('simple', 'test'),

    description = 'just a simple test of vipkid',

    license = 'MIT',

    author = 'mingrun',

    author_email = '13271929138@163.com',

    packages = find_packages(),

    platforms = 'any',

    py_modules=['transform.Transform_txt_xml']

)

