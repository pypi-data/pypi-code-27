from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wojak', 
version='0.2', 
description='request wojaks as a service', 
url='https://yakz.cf/', 
author='Jack (yak)', 
author_email='oganesson1@icloud.com', 
long_description=long_description, 
long_description_content_type='text/markdown', 
license='ABSE', 
packages=['wojak'], 
zip_safe=False, 
)