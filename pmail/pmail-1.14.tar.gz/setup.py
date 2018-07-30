from setuptools import setup

setup(
    name='pmail',
    version='1.14',
    description='Command-line e-mail sender',
    long_description=open('README.rst').read(),
    python_requires='>=3.5',
    url='https://bitbucket.org/tomaszwaraksa/pmail',
    author='Tomasz Waraksa',
    author_email='tomasz@waraksa.net',
    license='MIT',
    keywords='mail client e-mail email send',
    download_url="https://bitbucket.org/tomaszwaraksa/pmail/get/abd3be1798d3.zip",
    packages=['pmail'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Operating System :: OS Independent'
    ],
    install_requires=[
         'keyring'
    ],
    entry_points={
        "console_scripts":["pmail=pmail.commandline:main"]
    }
)
