import os
import hashlib
from os.path import isfile, isdir
import tempfile
import json
from .version import __version__


def _get_files_list(path, prefix):
    try:
        files = os.listdir(path)
        result_files = []
        for i in files:
            if isdir(path + i):
                result = _get_files_list(path + i + '/', prefix + i + '/')
                for r in result:
                    result_files.append(r)
            if isfile(path + i):
                result_files.append(prefix + i)
        return result_files
    except IOError:
        return []
    except OSError as e:
        print('Exception in [_get_files_list]:', e)
        return []


def get_files_list(path):
    return _get_files_list(path, '')


def create_dir_for_file(filename):
    path = filename
    k = path.rindex('/')
    path = path[:k]
    if not os.path.exists(path):
        os.makedirs(path)


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def normalize_path(path, append_slash=True):
    path = path.replace('\\', '/')
    if append_slash and path and path[-1] != '/':
        path += '/'
    return path


def load_dict(path):
    dictionary = {}
    try:
        file_ = open(path)
        for line in file_:
            string = line.strip()
            args = string.split(' ')
            if len(args) == 2:
                key = string.split(' ')[0]
                value = string.split(' ')[1]
                dictionary[key] = value
        return dictionary
    except IOError:
        return dictionary


def save_dict(path, dict_):
    try:
        dictionary = load_dict(path)
        for key in dict_:
            dictionary[key] = dict_[key]
        file_ = open(path, 'w')
        for key in dictionary:
            string = key + ' ' + dictionary[key] + '\n'
            file_.write(string)
    except IOError:
        return False
    return True


def write(path, content):
    rewrite = True
    if os.path.exists(path):
        rewrite = open(path).read() != content
    if rewrite:
        create_dir_for_file(path)
        open(path, 'w').write(content)
    return rewrite


_cache_file = tempfile.gettempdir() + '/bin/cache.{}.tmp'.format(__version__)


def file_has_changes(path):
    dictionary = load_dict(_cache_file)
    if path in dictionary:
        cache = dictionary[path]

        m = hashlib.md5()
        data = open(path, 'rb').read()
        try:
            m.update(data)
        except TypeError:
            m.update(data.encode('utf-8'))
        
        return not cache == str(m.hexdigest())
    return True


def save_md5_to_cache(path):
    create_dir_for_file(_cache_file)
    m = hashlib.md5()
    data = open(path, 'rb').read()
    try:
        m.update(data)
    except TypeError:
        m.update(data.encode('utf-8'))
    save_dict(_cache_file, {path: m.hexdigest()})


def has_changed_file(directory, ext=''):
    dictionary = load_dict(_cache_file)
    if directory in dictionary:
        cache = dictionary[directory]

        directory = directory.replace('\\', '/')
        if not directory.endswith('/'):
            directory += '/'
        files = get_files_list(directory)

        all_files = json.dumps(files)
        m = hashlib.md5()
        try:
            m.update(all_files)
        except TypeError:
            m.update(all_files.encode('utf-8'))
        if cache != str(m.hexdigest()):
            return True

        for file in files:
            if ext and not file.endswith(ext):
                continue
            if file_has_changes(directory + file):
                return True
        return False
    return True


def save_md5_of_files_in_directory(directory, ext=''):
    directory = directory.replace('\\', '/')
    if not directory.endswith('/'):
        directory += '/'
    files = get_files_list(directory)
    for file in files:
        if ext and not file.endswith(ext):
            continue
        save_md5_to_cache(directory + file)

    all_files = json.dumps(files)
    m = hashlib.md5()
    try:
        m.update(all_files)
    except TypeError:
        m.update(all_files.encode('utf-8'))
    save_dict(_cache_file, {directory: m.hexdigest()})
