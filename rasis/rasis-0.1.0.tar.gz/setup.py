from setuptools import setup, find_packages

setup(
    name='rasis',
    version='v0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'scrapy',
        'scrapy_splash',
        'pandas',
        'Pillow',
    ],
    entry_points='''
        [console_scripts]
        rasis=cmds.entry:entry
    ''',
)
