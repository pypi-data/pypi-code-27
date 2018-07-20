"""
Input output utilities
"""
import os
import shutil
import subprocess
import contextlib
import logging


def resolve(path):
    """
    Returns:
        path with resolved ~, symbolic links and relative paths.
    Examples:
        Resolves relative paths
        >>> import os
        >>> from tfields.lib.in_out import resolve
        >>> resolve("../tfields") == resolve(".")
        True

        Resolves user variables
        >>> resolve("~") == os.path.expanduser("~")
        True

        Also resolves symlincs which i will not test.
    """
    # return str(Path(path).expanduser().resolve())
    # resolve:       relative paths,  symlinks and    ~
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def cp(source, dest, overwrite=True):
    """
    copy with shutil
    """
    source = resolve(source)
    dest = resolve(dest)
    if os.path.isfile(dest) and not overwrite:
        raise ValueError("Attempting to overwrite destination path"
                         " {0}.".format(dest))
    if os.path.isfile(source):
        shutil.copy(source, dest)
    elif os.path.isdir(source):
        shutil.copytree(source, dest)
    else:
        raise TypeError("source is not file or dir")


def scp(source, dest):
    """
    ssh copy
    """
    # subprocess.check_call does not execute in bash, so it does not know ~
    # Carefull when giving remote host : ~ replacement is not tested
    subprocess.check_call(['scp', source, dest])


def mv(source, dest, overwrite=True):
    """
    Move files or whole folders
    """
    source = resolve(source)
    dest = resolve(dest)
    log = logging.getLogger()
    if os.path.isfile(dest) and not overwrite:
        raise ValueError("Attempting to move to already existing destination"
                         " path {0}.".format(dest))
    log.info("Moving file or dir {0} to {1}".format(source, dest))
    if os.path.isfile(source):
        shutil.move(source, dest)
    elif os.path.isdir(source):
        shutil.move(source, dest)
        # shutil.copytree(source, dest)
    else:
        raise TypeError("source is not file or dir")


def rm(path):
    """
    Remove path or (empty) directory
    """
    path = resolve(path)
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        if len(ls(path)) > 0:
            raise ValueError("Directory {0} is not empty".format(path))
        os.rmdir(path)
    else:
        raise ValueError("Path {0} is not directory and not file".format(path))


def cd(directory):
    """
    Change directory
    """
    os.chdir(resolve(directory))


@contextlib.contextmanager
def cd_tmp(tmpPath):
    """
    Temporarily change directory. change back afterwards
    """
    cwd = os.getcwd()
    cd(resolve(tmpPath))
    try:
        yield
    finally:
        cd(cwd)


def ls(directory, recursive=False):
    """
    a bash ls imitation.
    """
    if recursive:
        return dir_structure(resolve(directory))
    else:
        return os.listdir(resolve(directory))


def dir_structure(fileDir):
    """
    Creates a nested dictionary that represents the folder structure of fileDir
    """
    directory = {}
    fileDir = fileDir.rstrip(os.sep)
    start = fileDir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(fileDir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], directory)
        parent[folders[-1]] = subdir
    if len(directory) == 0:
        return {}
    return directory[directory.keys()[0]]  # first entry is always fileDir
