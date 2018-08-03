"""
Misc functions/classes/globals 

USERDIR/setup_log - to setup the logging and get user path for temp storage.
DictList          - a general purpose list/dict object supporting lookup via 
                    multiple keys.
"""
import logging
from logging import DEBUG,INFO,WARNING,ERROR
import os
import sys


#---Useful paths----------------------------------------------------------------
# This should probably be made more crossplatform and dependable by using
# sp = wx.StandardPaths_Get()
# sp.Get* methods.

#Resource dir (icons etc) stored  with in the package structure at the moment
#this should probably be changed at some point for linux/mac etc.
RESOURCE_DIR =  __file__.rpartition(os.sep)[0] +os.sep+ "resources"+os.sep

#check for and create a .ptk directory in the user home for options, logs and 
#command history
USERDIR = os.path.expanduser('~')+os.sep+'.ptk'+os.sep
if not os.path.exists(USERDIR):
    os.makedirs(USERDIR)
    if not os.path.exists(USERDIR):
        raise AssertionError('Cannot create .ptk options directory in home folder')

TOOLDIR = USERDIR+'tools'+os.sep
if not os.path.exists(TOOLDIR):
    os.makedirs(TOOLDIR)
    if not os.path.exists(TOOLDIR):
        raise AssertionError('Cannot create .ptk/tools directory in home folder')

#-------------------------------------------------------------------------------
def setup_log(filename, level=logging.INFO):
    """
    level - DEBUG,INFO,WARNING,ERROR
    """
    #setup logger
    logging.basicConfig(level=level,
                    format='%(asctime)s - %(name)-48s - %(levelname)-8s - %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S',
                    filename=filename,
                    filemode='w')

def open_help():
    """
    Open the PTK documentation
    """
    import webbrowser
    url='http://pythontoolkit.sourceforge.net/'
    webbrowser.open(url)

def get_config():
    """
    Get the wxconfig object used by ptk
    """
    import wx
    cfg = wx.FileConfig(localFilename=USERDIR+'options')
    return cfg
