"""
flask_redisosgearth
----------

A Flask extension for redis

Please refer to the online documentation for details.

"""
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='flask_redisosgearth',
    version='0.0.1',
    license='BSD',
    author='duoduoaixiaogai',
    author_email='490850477@qq.com',
    maintainer='duoduoaixiaogai',
    maintainer_email='490850477@qq.com',
    description='Flask extension for redis',
    long_description=long_description,
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
