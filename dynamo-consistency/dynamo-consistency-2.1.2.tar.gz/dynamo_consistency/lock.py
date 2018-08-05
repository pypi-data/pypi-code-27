"""
Performs simple file locking, and identifies which sites need them
"""

import os
import fcntl

from . import config

FHS = {}

def which(site):
    """
    Determine which lock is needed for a site from the config.

    :param str site: Site we want to lock for
    :returns: Name of the lock that should be acquired.
              If no lock to acquire, returns an empty string
    :rtype: str
    """

    method = config.config_dict().get('AccessMethod', {}).get(site)

    if method == 'SRM':
        return 'gfal'

    return ''


def acquire(lock):
    """
    This function will block until the named lock is acquired.
    :param str lock: Name of lock to acquire, which matches name in ``locks`` directory
    """

    FHS[lock] = open(os.path.join(os.path.dirname(__file__), 'locks', '%s.lock' % lock), 'w')
    fcntl.lockf(FHS[lock], fcntl.LOCK_EX)
    FHS[lock].write('%s\n' % os.getpid())


def release(lock):
    """
    :param str lock: Name of lock to release, which matches name in ``locks`` directory
    """

    FHS[lock].write('done\n')
    fcntl.lockf(FHS[lock], fcntl.LOCK_UN)
    FHS[lock].close()
