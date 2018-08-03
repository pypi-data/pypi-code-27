"""
Python distutils setup.py script:

Usage:
------

Install as a python package.
    $ python setup.py install

Other supported modes:
----------------------

Make source distribution (zip file for ease on windows and linux.)
    $ python setup.py sdist --format=zip

Make windows installer
    $ python setup.py bdist_wininst --install-script ptk_postinstall.py --user-access-control auto

Make a wheel
    $ python setup.py sdist bdist_wheel


Other distutils modes are currently unsupported. 
"""
import setuptools
from distutils.core import setup
import os
import shutil
import os.path
import sys

import ptk_lib

#-------------------------------------------------------------------------------
# Helper functions
#-------------------------------------------------------------------------------
def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


#-------------------------------------------------------------------------------
# Determine mode of operation and set scripts and package data to use
#-------------------------------------------------------------------------------
if sys.argv[1] == 'sdist':
    #building a source distribution add everything...
    SCRIPTS = ['PTK.pyw','PTKengine.pyw','windows/ptk_postinstall.py']
    PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                'resources/ptk.ico',
                                'resources/ptkicon.svg']}
    DATA_FILES =[ 
                ('.',[ 'README.txt','LICENSE.txt','CHANGES.txt']),
                ('.', ['linux/PTK.desktop']),
                ]

elif sys.argv[1] == 'bdist_wininst':
    #building a windows installer
    SCRIPTS = ['PTK.pyw','PTKengine.pyw','windows/ptk_postinstall.py']
    PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                'resources/ptk.ico',
                                'resources/ptkicon.svg']}
    DATA_FILES = []

    
elif sys.argv[1] == 'install':
    
    if sys.platform.startswith('win'):
        #installing on windows
        SCRIPTS = ['PTK.pyw','PTKengine.pyw','windows/ptk_postinstall.py']
        PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                    'resources/ptk.ico',
                                    'resources/ptkicon.svg']}
        DATA_FILES = []   

    elif sys.platform.startswith('darwin'):
        #On linux/mac we want to be able to type PTK to start the app using PTK
        #so make a copy and use that as the script
        shutil.copyfile('PTK.pyw', 'PTK')
        shutil.copyfile('PTKengine.pyw', 'PTKengine')
        SCRIPTS = ['PTK','PTKengine']

        PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                    'resources/ptk.ico',
                                    'resources/ptkicon.svg']}
        DATA_FILES = [ ]
        #TODO add mac launch script??? where does this go on a mac?
        
    else:
        #On linux/mac we want to be able to type PTK to start the app using PTK
        #so make a copy and use that as the script
        shutil.copyfile('PTK.pyw', 'PTK')
        shutil.copyfile('PTKengine.pyw', 'PTKengine')
        SCRIPTS = ['PTK','PTKengine']

        PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                    'resources/ptk.ico',
                                    'resources/ptkicon.svg']}
        DATA_FILES = [  ( '/usr/share/applications', ['linux/PTK.desktop'] ),
                        ( '/usr/share/pixmaps', ['ptk_lib/resources/ptkicon.svg']) ]
else:
    #unkown do everything
    SCRIPTS = ['PTK.pyw','PTKengine.pyw','windows/ptk_postinstall.py']
    PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                                'resources/ptk.ico',
                                'resources/ptkicon.svg']}
    DATA_FILES =[ 
                ('.',[ 'README.txt','LICENSE.txt','CHANGES.txt']),
                ('.', ['linux/PTK.desktop']),
                ]


#-------------------------------------------------------------------------------
# Collect data for the distutils setup() call.
#-------------------------------------------------------------------------------
VERSION = ptk_lib.VERSION
DESCRIP = "PythonToolkit (PTK) an interactive python environment"

LONG_DESCRIP = """PythonToolkit (PTK) is an interactive environment for python. 
It was designed to provide a python based environment similiar to Matlab
for scientists and engineers however it can also be used as a general
purpose interactive python environment."""

#Find packages to install
PACKAGES = find_packages(path='.', base="" )

#-------------------------------------------------------------------------------
#Do the python distutils setup
#-------------------------------------------------------------------------------

setup(
    name = 'PythonToolkit',
    version = VERSION,
    description = DESCRIP,
    long_description = LONG_DESCRIP,
    author = 'T.Charrett',
    author_email = 'tohc1@users.sourceforge.net',
    url = "http://pythontoolkit.sourceforge.net",
    packages = PACKAGES,
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License (GPL)"),
    scripts = SCRIPTS,
    package_data = PACKAGE_DATA,
    data_files = DATA_FILES)
