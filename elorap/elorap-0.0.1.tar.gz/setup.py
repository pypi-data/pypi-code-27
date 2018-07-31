import re as regexp

from setuptools import setup, find_packages

def main():
    setup(
        name='elorap',
        version='0.0.1',
        py_modules=[
            'elorap'
        ],
        packages=find_packages(),
        include_package_data=True,
        # The lowest supported Python 3 version is 3.5
        # please update accordingly iff changes
        python_requires=">2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
        install_requires=[
            'raven',
        ],
        extras_require={
            'dev': [
                'pytest',
                'pytest-mock'
            ]
        },
        entry_points='''
            [console_scripts]
            siemano=elorap.main:main
        ''',

        author="mua",
        description="Testing package",
        license="MIT",
        keywords="",
    )

if __name__ == "__main__":
    main()

