"""
PythonToolkit post install/uninstall script to add shorcuts in windows.
"""
import os
import sys
import _winreg as winreg #module renamed in python 3

import ctypes
from ctypes.wintypes import HWND, HANDLE, DWORD,LPCWSTR,MAX_PATH, create_unicode_buffer 

def get_special_folder(folder=0):
    """
    Get special folder path - version using ctypes!
    
    folder = 

    #public special folder constants
    DESKTOP                              0
    PROGRAMS                             2
    MYDOCUMENTS                          5
    FAVORITES                            6
    STARTUP                              7
    RECENT                               8
    SENDTO                               9
    STARTMENU                           11
    MYMUSIC                             13
    MYVIDEOS                            14
    NETHOOD                             19
    FONTS                               20
    TEMPLATES                           21
    ALLUSERSSTARTMENU                   22
    ALLUSERSPROGRAMS                    23
    ALLUSERSSTARTUP                     24
    ALLUSERSDESKTOP                     25
    APPLICATIONDATA                     26
    PRINTHOOD                           27
    LOCALSETTINGSAPPLICATIONDATA        28
    ALLUSERSFAVORITES                   31
    LOCALSETTINGSTEMPORARYINTERNETFILES 32
    COOKIES                             33
    LOCALSETTINGSHISTORY                34
    ALLUSERSAPPLICATIONDATA             35
    """
    SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
    SHGetFolderPath.argtypes = [HWND, ctypes.c_int, HANDLE, DWORD, LPCWSTR]
    auPathBuffer = create_unicode_buffer (MAX_PATH)
    exit_code=SHGetFolderPath(0, folder, 0, 0, auPathBuffer)
    return auPathBuffer.value

def create_startmenu_shortcut():
    """Create a startmenu shortcut"""
    #make the ptk folder
    programs = get_special_folder(23)
    ptk_dir = programs+'\\PythonToolkit(PTK)'
    os.mkdir( ptk_dir)
    directory_created(ptk_dir)

    #create the shortcut
    target = sys.prefix+'\\pythonw'
    description = 'Start PythonToolkit (PTK)'
    filename = ptk_dir+'\\PythonToolkit(PTK).lnk'
    args = sys.prefix+'\\Scripts\\PTK.pyw'
    icon = sys.prefix+'\\Lib\\site-packages\\ptk_lib\\resources\\ptk.ico'
    create_shortcut(target, description, filename,args,sys.prefix,icon)
    file_created(filename)

def add_filetypes():
    """
    Associate PTK with python files in the registry
    """
    #build command
    prefix = os.path.normpath(sys.prefix)
    cmd = '"'+prefix+os.sep+'pythonw.exe" "'+prefix+os.sep+'\scripts\PTK.pyw" -f "%1"'

    #.py
    #HKEY_CLASSES_ROOT\Python.File\shell\Edit with PTK\command
    #   default = "c:\python27\pythonw.exe" "c:\python27\scripts\PTK" -f "%1"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.File\shell\Edit with PTK\command")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
    winreg.CloseKey(key)

    #.pyw
    #HKEY_CLASSES_ROOT\Python.NoConFile\shell\Edit with PTK\command
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.NoConFile\shell\Edit with PTK\command")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ,cmd)
    winreg.CloseKey(key)
    
def remove_filetypes():
    #.py
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.File\shell\Edit with PTK\command")
    winreg.DeleteKey(key,'')
    winreg.CloseKey(key)
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.File\shell\Edit with PTK")

    winreg.DeleteKey(key,'')
    winreg.CloseKey(key)

    #.pyw
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.NoConFile\shell\Edit with PTK\command")

    winreg.DeleteKey(key,'')
    winreg.CloseKey(key)
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Python.NoConFile\shell\Edit with PTK")
    winreg.DeleteKey(key,'')
    winreg.CloseKey(key)

##Main script ----------------------------------------------------------------------------------------
if sys.argv[1] == '-install':
    print "PythonToolkit installed sucessfully (run python2.X\scipts\PTK.pyw to launch)"

    #create a startmenu folder for PTK.
    print 'Attempting to create shortcuts'
    try:
        create_startmenu_shortcut()
    except:
        print 'Failed to create start menu shortcuts (to start PTK execute python\scripts\PTK.pyw)'
        raise        

    ##add registry entries for file associations
    print 'Atttempting to add file types associations'
    try:
        add_filetypes()
    except:
        print 'Failed to associate PTK with file types'
        raise

else:
    ##remove windows registry file association entries.
    try:
        remove_filetypes()
    except:
        print 'Failed to deregister file types'
        raise

    ##Startmenu shortcuts are removed automatically
    ##as they are added using file_created/directory_created

