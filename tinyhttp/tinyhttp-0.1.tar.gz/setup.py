from setuptools import setup

setup(
    name='tinyhttp',
    version='0.1',
    author='Wincer',
    author_email='WincerChan@gmail.com',
    url='https://github.com/WincerChan/Tiny-Http',
    description='Async static HTTP server.',
    packages=['tinyhttp'],
    license='GPL-3.0',
    entry_points={
        'console_scripts': [
            'tinyhttp=tinyhttp.async.asyncserver:main'
        ]
    }
)
