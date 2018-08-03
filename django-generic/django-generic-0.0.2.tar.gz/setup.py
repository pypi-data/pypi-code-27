from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name='django-generic',
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    test_suite="runtests.runtests",
    include_package_data=True,
    description='Generic helpers for Django framework',
    long_description=read('README.md'),
    url='https://github.com/maledorak/django-generic',
    author='Mariusz Korzekwa',
    python_requires=">=3.4",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
