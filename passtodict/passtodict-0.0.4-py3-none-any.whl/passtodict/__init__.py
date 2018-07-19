# Copyright (C) 2018  Pachol, Vojtěch <pacholick@gmail.com>
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
import gnupg


__all__ = ['get']

PASS_PATH = os.path.expanduser('~/.password-store/')
gpg = gnupg.GPG()


class DecryptError(Exception):
    pass


class Fields(dict):
    """Dict with password fields. Password itself is in `fields.PWD`"""
    def __init__(self, string: str):
        lines = string.splitlines()
        self.PWD = lines.pop(0)
        self.extra = []

        for line in lines:
            key, sep, value = line.partition(':')
            if sep:
                self[key] = value.lstrip()
            else:
                self.extra.append(line)


def get(passname):
    with open(PASS_PATH + passname + '.gpg', 'rb') as f:
        crypt = gpg.decrypt_file(f)

    if not crypt:
        raise DecryptError(crypt.status)

    info = str(crypt)
    return Fields(info)
