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

import subprocess


class TestCaissa:
    """
    Test Caissa class
    """

    def test_main(self):
        """
        Test main application
        """

        import time

        args = "--debug --daemon --play-radio"

        proc = subprocess.Popen(
            "/usr/bin/env python3 -m caissa " + args,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True)

        try:
            # try out the following sequence of text inputs
            text_inputs = ["play radio", "next", "prev", "stop radio"]

            for text_input in text_inputs:
                time.sleep(4)
                proc.stdin.write(text_input + "\n")
                proc.stdin.flush()

            # try out the following sequence of infrared inputs
            ir_inputs = ["KEY_PLAY", "KEY_NEXT", "KEY_PREVIOUS", "KEY_PLAY",
                         "KEY_VOLUMEUP", "KEY_VOLUMEDOWN"]

            for ir_input in ir_inputs:
                self._simulate_ir_event(ir_input)
                time.sleep(0.5)

            outs, errs = proc.communicate("exit\n", timeout=2)

            # check if all went well
            assert "Bringing Caissa to life" in errs
            assert "Playing radio station" in errs
            assert ("Setting volume to" in errs or
                    "No suitable mixer found, cannot change volume." in errs)
            assert "Constructed new infrared input event" in errs
            assert "Processing text input event \"exit\"" in errs

        except subprocess.TimeoutExpired:
            import pytest

            pytest.fail("Process did not exit cleanly (timeout reached)!")

    def _simulate_ir_event(self, key):
        """
        Simulate an infrared event (remote key press)
        """

        subprocess.run(
            ["irsend", "simulate",
             "0000000000000000 00 {} my_remote".format(key)])


if __name__ == "__main__":
    tester = TestCaissa()
    tester.test_main()
