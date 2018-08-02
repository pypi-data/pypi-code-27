from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setup(
    name='skype_chatbot',
    version='1.0.3',
    packages=find_packages(),
    description='API for development the Skype chat-bot',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
    keywords='skype chat-bot chatbot bot api',
    url='',
    author='Anton Kotseruba',
    author_email='ghost8recon@gmail.com',
    license='MIT',
    install_requires=[
        'requests>=2.18.4',
    ],
    include_package_data=True,
    zip_safe=False
)
