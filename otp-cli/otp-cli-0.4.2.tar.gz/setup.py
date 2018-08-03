from setuptools import setup
import sys

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "otp-cli",
    version = "0.4.2",
	description = "A CLI one-time password application that manages one-time passwords elegantly and with tons of customization.", 
	author = "Nathan Yan",
	author_email = "nathancyan2002@gmail.com",
	url = "https://github.com/nathan-yan/otp_",
    py_modules = ["otp", "delete", "write", "show", "update", "getch_" ],
    install_requires = requirements,
    entry_points = '''
    [console_scripts]
    otp=otp:cli
    '''
)
