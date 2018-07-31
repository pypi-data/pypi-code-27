#!/usr/bin/env python3

"""Sorting files by time, made easy.

    Gets last modification time from file(s) and folder(s), 
    then moves them to a new directory, sorting them in new
    folders.  These folder names are in 'yyyy-mm-dd' format.
"""

import os
import time
import shutil
import errno
from datetime import datetime


def mtmove(src, dst):
    """
    Moves files/folders & puts them in folders by last modified date.

    Example:
    
    >>> import mtsort
    >>> mtsort.mtmove('/home/test/sourcedir', '/home/test/destdir')

    before:                after:
    .                      .
    |-- destdir            |-- destdir
    |-- sourcedir          |   |-- 2016-07-29  
        |-- file1          |   |   |-- file1
        |-- file2          |   |-- 2016-07-30
        |-- file3          |   |   |-- file2
                           |   |-- 2016-07-31
                           |       |-- file3
                           |-- sourcedir

    
    On Windows machines, this function will raise an Exception if the
    source and dest. paths are on different drives, this was done as a
    precaution due to unexpected behaviour. To get around this, just use
    mtcopy instead.
    """
    # Make sure moving is local only (may only work on Windows)
    if os.path.isdir(src) and os.path.isdir(dst):
        pathsrc = os.path.abspath(src)
        pathdst = os.path.abspath(dst)
        if os.path.splitdrive(pathsrc)[0] != os.path.splitdrive(pathdst)[0]:
            raise UserWarning('For transferring files to a different drive, '
                              'use the copy function.')
    else:
        raise NotADirectoryError('The path(s) entered dont exist, '
                                 'please try again')
    os.chdir(src)
    gen_time = (time.ctime(os.path.getmtime(x)) for x in os.listdir(src))
    time_list = list(gen_time)
    # Map mtime (in time format) to abbreviated date
    date_dic = {x: datetime.strptime(x[4:10] + x[-4:], '%b %d%Y')
                .strftime('%Y-%m-%d') for x in time_list}
    # Make folders with name of dates
    for w in date_dic.values():
        os.makedirs(dst + '/' + w, exist_ok=True)
    for x in os.listdir(src):
        if time.ctime(os.path.getmtime(x)) in date_dic.keys():
            path = dst + '/' + date_dic.get(time.ctime(os.path.getmtime(x)))
            # This will move all files/directories recursively
            try:
                shutil.move(x, path + '/' + x)
            except PermissionError:
                print('You dont have the right Permissions to move: ' + x)


def mtcopy(src, dst):
    """
    Copies files/folders & puts them in folders by last modified date.

    Example:
    
    >>> import mtsort
    >>> mtsort.mtcopy('/home/test/sourcedir', '/home/test/destdir')

    before:                after:
    .                      .
    |-- destdir            |-- destdir
    |-- sourcedir          |   |-- 2016-07-29  
        |-- file1          |   |   |-- file1
        |-- file2          |   |-- 2016-07-30
        |-- file3          |   |   |-- file2
                           |   |-- 2016-07-31
                           |       |-- file3
                           |-- sourcedir
                               |-- file1
                               |-- file2
                               |-- file3
    """
    if not os.path.isdir(src) or not os.path.isdir(dst):
        raise NotADirectoryError('The path(s) entered dont exist, '
                                 'please try again')
    os.chdir(src)
    gen_time = (time.ctime(os.path.getmtime(x)) for x in os.listdir(src))
    time_list = list(gen_time)
    # Map mtime (in time format) to abbreviated date
    date_dic = {x: datetime.strptime(x[4:10] + x[-4:], '%b %d%Y')
                .strftime('%Y-%m-%d') for x in time_list}
    # Make folders with name of dates
    for w in date_dic.values():
        os.makedirs(dst + '/' + w, exist_ok=True)
    for x in os.listdir(src):
        if time.ctime(os.path.getmtime(x)) in date_dic.keys():
            path = dst + '/' + date_dic.get(time.ctime(os.path.getmtime(x)))
            # Copy all directories recursively
            try:
                shutil.copytree(x, path + '/' + x)
            except PermissionError:
                print('You dont have the right Permissions '
                      'to copy the folder: ' + x)
            except OSError as exc:
                # If not a directory, copy the file(s)
                if exc.errno == errno.ENOTDIR:
                    try:
                        shutil.copy2(x, path + '/' + x)
                    except PermissionError:
                        print('You dont have the right Permissions '
                              'to copy the file:  ' + x)

def main():
    print('This script moves/copies all files & folders, then puts them in '
          'folders by their last modified date.')
    print()
    while True:
        a1 = input('Move or copy? (m/c): ')
        if a1 == 'm' or a1 == 'move':
            while True:
                c1 = input('Source directory: ')
                if os.path.isdir(c1):
                    print()
                    break
                else:
                    print('Directory not found.')
                    
            while True:
                c2 = input('Destination directory: ')
                if os.path.isdir(c2):
                    print()
                    break
                else:
                    print('Directory not found.')
            try:        
                mtmove(c1, c2)
            except UserWarning:
                print('Moving files between different drives wont work, '
                      'use copy instead.')
                break
            print()
            fin = input('Done! Press ENTER to exit. ') 
            break

        if a1 == 'c' or a1 == 'copy':
            while True:
                c3 = input('Source directory: ')
                if os.path.isdir(c3):
                    print()
                    break
                else:
                    print('Directory not found.')

            while True:
                c4 = input('Destination directory: ')
                if os.path.isdir(c4):
                    print()
                    break
                else:
                    print('Directory not found.')

            mtcopy(c3, c4)
            print()
            fin = input('Done! Press ENTER to exit. ')
            break
        
if __name__ == '__main__':
    main()
