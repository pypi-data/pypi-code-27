#pylint: disable=missing-docstring, unused-argument, invalid-name

"""
This module defines dummy variables as needed by
dynamo_consistency.backend for running tests with
"""


import os


# These are all the methods needed from inventory
class _Inventory(object):
    @staticmethod
    def protected_datasets(site):
        return set()
    @staticmethod
    def list_files(site):
        return list()
    @staticmethod
    def filelist_to_blocklist(site, infile, outfile):
        pass


class _Registry(object):
    @staticmethod
    def delete(site, files):
        return len(files)
    @staticmethod
    def transfer(site, files):
        return [], []


class _SiteInfo(object):
    @staticmethod
    def site_list():
        return ['TEST_SITE', 'BAD_SITE']
    @staticmethod
    def ready_sites():
        return set(['TEST_SITE'])


def _ls(path, location='tmp'):

    full_path = os.path.join(location, path)
    results = [os.path.join(full_path, res) for res in os.listdir(full_path)]

    dirs = [(os.path.basename(name), os.stat(name).st_mtime)
            for name in results if os.path.isdir(name)]
    files = [(os.path.basename(name), os.stat(name).st_size, os.stat(name).st_mtime)
             for name in results if os.path.isfile(name)]

    return True, dirs, files


# The following are all the things imported by dynamo_consistency.backend

inventory = _Inventory()
registry = _Registry()
siteinfo = _SiteInfo()

def get_listers(site):
    return _ls, None

def check_site(site):
    return site in siteinfo.ready_sites()

def deletion_requests(site):
    return set()

class DatasetFilter(object):
    def __init__(self, _):
        pass
    @staticmethod
    def protected(_):
        return False
