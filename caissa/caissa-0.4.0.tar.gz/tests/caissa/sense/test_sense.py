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


class TestSense:
    """
    Tests for sense module
    """

    def test_lirc_config(self):
        """
        Generate and lirc config file and check its contents
        """

        from caissa.sense.lirc_config import get_lircrc_filename

        filename = get_lircrc_filename()

        # read the file
        with open(filename) as file:
            import re

            pattern = re.compile(r"begin|end|"
                                 r"\s+prog = caissa|"
                                 r"\s+button = \S+|"
                                 r"\s+config = \S+|"
                                 r"\s+repeat = [0-9]+")

            for line in file:
                assert re.fullmatch(pattern, line.rstrip()) is not None
