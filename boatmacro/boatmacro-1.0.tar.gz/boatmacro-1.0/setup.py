from setuptools import setup, find_packages

setup_requires = [
    ]

install_requires = [
    ' pypiwin32==223'
    ]

dependency_links = [
    ]

setup(
    name='boatmacro',
    version='1.0',
    description='Macro in python | auto do',
    author='BoatonBoat',
    author_email='usbjewon@gmail.com',
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=dependency_links,
    # scripts=['manage.py'],
    entry_points={
        'console_scripts': [
            ],
        "egg_info.writers": [
                
            ],
        },
    )