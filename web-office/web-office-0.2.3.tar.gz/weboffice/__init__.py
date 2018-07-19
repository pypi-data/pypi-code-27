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
import sys
import shutil
import git
from urllib.parse import quote
import webbrowser
import re
from time import time

from weboffice.progressbar import Pulsate


GIT_REPO = os.path.expanduser("~/.local/share/web-office-files")
github_raw_url = "https://github.com/pacholik/web-office-files/raw/master/%s"
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
        dst = os.path.basename(src)

    try:
        os.link(src, dst)
    except OSError:
        try:
            shutil.copy(src, dst)
        except shutil.Error:
            pass


class Github:
    def __init__(self):
        try:
            self.repo = git.Repo(GIT_REPO)
        except git.exc.InvalidGitRepositoryError:
            sys.exit("Please clone your repository to {}.".format(GIT_REPO))

        self.origin = self.repo.remote()
        self.index = self.repo.index

        self.origin.pull()
        # delete older than two weeks
        if self.index.entries:
            self.index.remove(
                [filename for filename, number in self.index.entries if
                 time() - os.path.getmtime(os.path.join(GIT_REPO, filename)) >
                 3600*24*14],
                working_tree=True)

    def get_raw_url(self):
        origin_url = next(self.origin.urls)
        return ("https://github.com/" +
                re.match(r'.*:(.*)\.git', origin_url).group(1) +
                "/raw/master/%s")

    def push(self, filenames):
        """Add files to repo, commit and push.

        :param filenames:   List of paths to the files
        :returns:           URLs of the files
        """
        if len(filenames) == 0:
            raise ValueError("Can't push an emty list.")

        filenames = [os.path.abspath(i) for i in filenames]
        basenames = [os.path.basename(i) for i in filenames]
        os.chdir(GIT_REPO)
        for f in filenames:
            link_or_copy(f)

        self.repo.index.add(basenames)
        self.repo.index.commit(COMMIT_MESSAGE)

        self.origin.push()

        for i in basenames:
            yield self.get_raw_url() % quote(i)


@Pulsate
def main(service="msoo"):
    github = Github()
    file_urls = github.push(sys.argv[1:])

    service_url = SERVICES.get(service, SERVICES['msoo'])

    for u in file_urls:
        u = service_url % quote(u)
        print(u)
        webbrowser.open(u)


def msoo():
    main("msoo")


def gdocs():
    main("gdocs")


if __name__ == "__main__":
    sys.argv.append("/home/pacholik/scores/Cry me a river.doc")
    main()
