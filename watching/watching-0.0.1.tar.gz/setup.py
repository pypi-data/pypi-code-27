from setuptools import setup

PACKAGE_VERSION = '0.0.1'
PACKAGE_REQUIRES = [
    'pygithub==1.40',
]
DEVELOPMENT_STATUS = '5 - Production/Stable'

setup(
    name='watching',
    version=PACKAGE_VERSION,
    description='github repo watching client .',
    url='https://github.com/joway/repo-watching',
    author='Joway Wang',
    author_email='joway.w@gmail.com',
    license='MIT',
    packages=['watching'],
    keywords='github repo watching robot framework',
    install_requires=PACKAGE_REQUIRES,
    classifiers=[
        'Development Status :: %s' % DEVELOPMENT_STATUS,
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
