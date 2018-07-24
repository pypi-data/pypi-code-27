from setuptools import setup, find_packages

VERSION = '0.1.3'

setup(
    name='piyon',
    description='a tiny cli to create a python project with pytest and basic pytest plugins',
    keywords='python pytest',
    version=VERSION,

    author='kiyon',
    author_email='kiyonlin@gmail.com',
    url='https://github.com/kiyonlin/piyon',

    packages=find_packages('src'),  # 包含所有src中的包
    package_dir={'': 'src'},  # 告诉distutils包都在src下

    package_data={
        'piyon': [
            'template/.gitignore',
            'template/*',
            'template/**/**',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        'pytest-mock'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
        'pytest-flakes',
    ],
    entry_points={
        'console_scripts': [
            'piyon = piyon:main.run'
        ]
    }
)
