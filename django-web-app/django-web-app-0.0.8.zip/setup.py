# _*_ coding:utf-8 _*_
__author__ = 'WANGY'
__date__ = '2018/8/1 19:02'

import re
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = ''
with open('web_app/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

with open('CHANGELOG.rst', 'rb') as f:
    changelog = f.read().decode('utf-8')

setup(
    name='django-web-app',
    version=version,
    description='a django web app',
    long_description='\n\n'.join([readme, changelog]),
    platforms=['Unix', 'Windows', 'MacOS'],
    url='https://gitee.com/upcwangying/UpcwangyingWebApp',
    author='Ying Wang',
    author_email='upcwangying@126.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='upcwangying wangying upc django web app',
    project_urls={
        'Documentation': 'https://docs.upcwangying.com/',
        'Source': 'https://gitee.com/upcwangying/UpcwangyingWebApp',
    },
    packages=['web_app'],
    install_requires=['django>=1.10'],
    include_package_data=True,
    zip_safe=False,
)
