#!/usr/bin/python3

# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import os
from os import path
import shutil
import sys
import git
from urllib.parse import quote
import re
from time import time


GIT_REPO = path.expanduser("~/.local/share/web-office-files")
COMMIT_MESSAGE = "Automatic"

SERVICES = {
    "gdocs":    "http://docs.google.com/viewer?url=%s",
    "msoo":     "http://view.officeapps.live.com/op/view.aspx?src=%s"
}


def link_or_copy(src, dst=None):
    """Try to create hardlink. In case it's impossible, create copy.

    :param src: Source
    :param dst: Destination
    """
    if not dst:
        dst = path.basename(src)

    try:
        os.link(src, dst)
    except OSError:
        shutil.copy(src, dst)


class Github:
    def __init__(self):
        try:
            self.repo = git.Repo(GIT_REPO)
        except git.exc.InvalidGitRepositoryError:
            sys.exit("Please clone your repository to {}.".format(GIT_REPO))

        self.origin = self.repo.remote()
        self.origin_url = next(self.origin.urls)
        self.index = self.repo.index

        # remove all posible unstashed changes and pull
        self.index.reset(working_tree=True)
        self.origin.pull()
        # delete older than two weeks
        oldfiles = [
            filename for filename, number in self.index.entries if
            time() - path.getmtime(path.join(GIT_REPO, filename)) > 3600*24*14
        ]
        if oldfiles:
            self.index.remove(oldfiles, working_tree=True, f=True)

    def get_raw_url(self, filename):
        """Return raw file url on Github."""
        return "https://github.com/{}/raw/master/{}".format(
            re.match(r'.*:(.*)\.git', self.origin_url).group(1),
            quote(filename))

    def push(self, filenames):
        """Add files to repo, commit and push.

        :param filenames:   List of paths to the files
        :returns:           URLs of the files
        """
        if len(filenames) == 0:
            raise ValueError("Can't push an emty list.")

        filenames = [path.abspath(i) for i in filenames]
        basenames = [path.basename(i) for i in filenames]
        os.chdir(GIT_REPO)
        for f in filenames:
            link_or_copy(f)

        self.index.add(basenames)
        self.index.commit(COMMIT_MESSAGE)

        self.origin.push()

        for i in basenames:
            yield self.get_raw_url(i)
