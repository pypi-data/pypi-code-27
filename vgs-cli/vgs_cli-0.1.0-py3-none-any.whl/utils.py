import os
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def is_file_accessible(path, mode='r'):
    file_exists = os.path.exists(path) and os.path.isfile(path)
    if not file_exists:
        return False

    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True
