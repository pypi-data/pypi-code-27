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

import sys
from urllib.parse import quote
import webbrowser

from weboffice.githosting import GitLab
from weboffice.progressbar import Pulsate


VIEWERS = {
    "gdocs":    "http://docs.google.com/viewer?url=%s",
    "msoo":     "http://view.officeapps.live.com/op/view.aspx?src=%s"
}


@Pulsate
def main(service="msoo"):
    github = GitLab()
    file_urls = github.push(sys.argv[1:])

    service_url = VIEWERS.get(service, VIEWERS['msoo'])

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
