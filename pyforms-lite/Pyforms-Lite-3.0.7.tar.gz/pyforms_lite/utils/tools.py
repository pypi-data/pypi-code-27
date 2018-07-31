#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import os
import sys
import zipfile
from subprocess import Popen, PIPE
import subprocess


def getFileInSameDirectory(file, name):
	module_path = os.path.abspath(os.path.dirname(file))
	return os.path.join(module_path, name)


def get_object_class_path(obj):
	path = os.path.abspath(sys.modules[obj.__module__].__file__)
	head, tail = os.path.split(path)
	return head


def zipdir(path, zippath):
    """
    walkfiles = os.walk(path)
    zippath = zipfile.ZipFile(zippath, 'w')
    for root, dirs, files in walkfiles:
        for filename in files: zippath.write(os.path.join(root, filename))
    """
    execStr = ['zip', '-r',zippath, path]
    print(' '.join(execStr))
    proc = subprocess.Popen(execStr, stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    if error: print ('error: '+ error)
    print('output: '+ output)
        

def zipfiles(files, zippath):
    zippath = zipfile.ZipFile(zippath, 'w')
    for filename in files: zippath.write( filename)
