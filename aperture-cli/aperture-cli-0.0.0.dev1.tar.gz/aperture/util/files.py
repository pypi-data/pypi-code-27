import os
import math
from aperturelib import SUPPORTED_EXTENSIONS

DEFAULT_RECURSION_DEPTH = 0
MAX_RECURSTION_DEPTH = 10
DEFAULT_DIR = os.getcwd()


##############################################################
# Returns paths to all files from a provided path. Recursively
# traverses subdirectories up to a given depth, retrieving
# files from those directories as well.
##############################################################
def get_files_in_directory_recursive(directory, max_depth=MAX_RECURSTION_DEPTH):
    files = []

    def do_scan(start_dir, output, depth=0):
        #Using scandir here instead of listdir. They do the same thing but
        # scandir has fewer stat() calls and so is much faster
        for entry in os.scandir(start_dir):
            if entry.is_dir(follow_symlinks=False):
                if depth < max_depth:
                    do_scan(entry.path, output, depth + 1)
            else:
                output.append(entry.path)

    do_scan(directory, files, depth=0)
    return files


##############################################################
# From an integer of bytes, convert to human readable format
# and return a string.
##############################################################
def bytes_to_readable(bytes):
    if bytes < 0:
        return '<0 B '
    elif bytes == 0:
        return '0 B '
    else:
        mem_sizes = ('B ', 'KB', 'MB', 'GB', 'TB')
        level = math.floor(math.log(bytes, 1024))
        return '{:.2f} {}'.format(bytes / 1024**level, mem_sizes[level])


def get_file_size_comparison(old_path, new_path):
    old_size = os.path.getsize(old_path)
    new_size = os.path.getsize(new_path)
    return (old_size, new_size)