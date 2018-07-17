from setuptools import setup, find_packages

setup(
    name='random_name_generator',
    version='1.0.3',
    packages=find_packages(exclude=['contrib', 'docs']),
    python_requires='~=3.6',
    url='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='Random Names Generator',
    install_requires=[]

)
