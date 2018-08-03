# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=72 cc=+8
"""\
Recipe visaplan.recipe.symlinks:
Create symbolic links to Zope resources
"""

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"

from os import makedirs, symlink, readlink, unlink
from os.path import (normpath, abspath, relpath,
        exists, isdir, islink,
        )
from logging import getLogger

from visaplan.recipe.symlinks.utils import (
        check_ternary_value, ternary_bool,
        check_directory, check_symlink,
        symlink_clone,
        )


class Recipe:
    """
    zc.buildout recipe to create symbolic links
    """

    def __init__(self, buildout, name, options):

        self.buildout, self.name, self.options = buildout, name, options
        self.logger = getLogger(self.name)

        key = 'document-root'
        docroot = options.get(key)
        if not docroot:
            docroot = options[key] =\
                    normpath(join(buildout['buildout']['parts-directory'],
                                  'htdocs'))
        check_directory(docroot, key=key)

        check_ternary_value('link-leaves',
                            options,
                            allowed=['yes', 'no', 'auto'],
                            implemented=['yes', 'no'])
        check_ternary_value('relative-links',
                            options,
                            allowed=['yes', 'no'],
                            implemented=['yes', 'no'])

    def install(self):
        """
        Create the symbolic resource links, according to the options.

        Return the paths of the directories and symlinks created.
        """
        options = self.options
        link_leaves = ternary_bool(options['link-leaves'])
        relative_links = ternary_bool(options['relative-links'])
        created = options.created

        key = 'document-root'
        docroot = options[key]
        if check_directory(docroot, key=key):
            created(docroot)
            makedirs(docroot)

        for pkg in self.given_packages():
            # TODO: if link_leaves is None ('auto'),
            #       detect development packages
            # TODO: detect resource specs!
            for (resourcename, fullpath) in self.resource_dir_tuples(pkg):
                clonepath = join(docroot, '++resource++'+resourcename)
                if not isdir(fullpath) or not link_leaves:
                    # TODO: if <clonepath> is a symlink clone, remove it
                    if relative_links:
                        target = relpath(fullpath, docroot)
                    else:
                        target = abspath(fullpath)
                    if check_symlink(clonepath, target):
                        created(clonepath)
                        symlink(target, clonepath)
                else:  # isdir and link_leaves
                    if islink(clonepath):
                        unlink(clonepath)
                    symlink_clone(fullpath,
                                  clonepath,
                                  relative=relative_links,
                                  created,
                                  pkg=pkg)

        return created()

    update = install
