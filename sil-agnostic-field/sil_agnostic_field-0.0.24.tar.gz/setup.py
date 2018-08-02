from setuptools import setup

name = 'sil_agnostic_field'
version = '0.0.24'
desc = 'A database independent django model field'


setup(
    name=name,
    version=version,
    description=desc,
    url="http://pip.slade360.co.ke/docs/{}/".format(name),
    author='SIL',
    author_email='developers@savannahinformatics.com',
    license="Proprietary",
    packages=['sil_agnostic_field'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'django>=2.0.0,<2.1.0',
        'djangorestframework==3.8.2',
    ]
)
