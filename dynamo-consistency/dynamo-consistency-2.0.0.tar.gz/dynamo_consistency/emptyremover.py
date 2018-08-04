"""
Defines a class that can remove nodes from a :py:class:`DirectoryInfo` object
"""

import logging

from os.path import join

from . import datatypes
from .backend import registry


LOG = logging.getLogger(__name__)


class EmptyRemover(object):
    """
    This class handles the removal of empty directories from the tree
    by behaving as a callback.
    It also calls deletions for the registry at the same time.
    :param str site: Site name. If value is ``None``, then don't enter deletions
                     into the registry, but still remove node from tree
    :param function check: The function to check against orphans to not delete.
                           The full path name is passed to the function.
                           If it returns ``True``, the directory is not deleted.
    """

    def __init__(self, site, check=None):
        self.site = site
        self.check = check or (lambda _: False)
        self.removed = 0

    def __call__(self, tree):
        """
        Removes acceptable empty directories from the tree
        :param tree: The tree that is periodically cleaned by this
        :type tree: :py:class:`datatypes.DirectoryInfo`
        """
        tree.setup_hash()
        empties = [empty for empty in tree.empty_nodes_list()
                   if not self.check(join(tree.name, empty))]

        not_empty = []

        for path in empties:
            try:
                tree.remove_node(path)
            except datatypes.NotEmpty as msg:
                LOG.warning('While removing %s: %s', path, msg)
                not_empty.append(path)

        for path in not_empty:
            empties.remove(path)

        self.removed += registry.delete(self.site, empties) if self.site else len(empties)

    def get_removed_count(self):
        """
        :returns: The number of directories removed by this function object
        :rtype: int
        """
        return self.removed
