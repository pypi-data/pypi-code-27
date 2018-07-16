# -*- coding: utf-8 -*-
"""
Caissa voice-controlled personal assistant
Copyright © 2018  Dieter Dobbelaere

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tempfile


def get_lircrc_filename(prog="caissa"):
    """
    Generate an lircrc file on-the-fly, return its filename
    """

    keys = ["KEY_UP", "KEY_DOWN"]
    keys += ["KEY_NEXT", "KEY_PREVIOUS"]
    keys += ["KEY_PLAY"]
    keys += ["KEY_VOLUMEUP", "KEY_VOLUMEDOWN"]

    # add the wild card key as last
    keys += ["*"]

    # add key options here
    options = {}
    options["KEY_VOLUMEUP"] = [("repeat", "3")]
    options["KEY_VOLUMEDOWN"] = [("repeat", "3")]

    # generate the file
    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)

    for key in keys:
        fp.write("begin\n")
        fp.write("    prog = {}\n".format(prog))
        fp.write("    button = {}\n".format(key))
        fp.write("    config = {}\n".format(key))

        for option, value in options.get(key, []):
            fp.write("    {} = {}\n".format(option, value))

        fp.write("end\n")

    return fp.name
