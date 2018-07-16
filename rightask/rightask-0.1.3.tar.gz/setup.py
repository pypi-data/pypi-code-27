from setuptools import setup, find_packages

setup(
     name='rightask',    # This is the name of your PyPI-package.
     version='0.1.3', # Update the version number for new releases
     author= 'bersub',
     author_email = 'bernardosubercaseaux@gmail.com',
     url='https://github.com/bsubercaseaux/rightask',
     packages=['rt'],
     entry_points = {
         'console_scripts': [
             'rt = rt.__main__:main'
        ]
    }              # The name of your scipt, and also the command you'll be using for calling it
)
