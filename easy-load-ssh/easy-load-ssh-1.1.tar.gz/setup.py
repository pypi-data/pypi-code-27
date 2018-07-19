from setuptools import setup, find_packages

setup(
    name='easy-load-ssh',
    version='1.1',
    license='GPLv3',
    packages=['elssh'],
    author='John Frederick Cornish IV',
    author_email='johncornishthe4th@gmail.com',
    install_requires=[
        'click',
        'PyYAML',
    ],
    entry_points='''
    [console_scripts]
    elssh=elssh:cli
    '''
)
