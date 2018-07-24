# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from os import kill
from signal import SIGTERM
from subprocess import check_output, CalledProcessError

from buildok.action import Action


class KillProcess(Action):
    r"""Send SIGTERM signal to a process.

    Args:
        pid (int): Process ID.
        pname (str): Process name.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `pid` or `pname` is provided.
        CalledProcessError: If `pname` is not found.

    Accepted statements:
        ^(?:kill|stop) process `(?P<pname>.+)`$
        ^(?:kill|stop) pid `(?P<pid>.+)`$

    Sample (input):
        - Stop process `someProcessName`.

    Expected:
        Terminated process PID => 9999
    """

    def run(self, pid=None, pname=None, *args, **kwargs):
        try:
            if pname is not None:
                pid = check_output(["pidof", "-s", pname])
            if pid is None:
                raise ValueError("Invalid PID")
            kill(int(pid), SIGTERM)
            self.susccess("Terminated process PID => %s" % pid)
        except OSError as e:
            self.fail(str(e))
        except ValueError as e:
            self.fail(str(e))
        except CalledProcessError as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, pid=None, pname=None, *args, **kwargs):
        if pid is not None:
            return "kill %s" % pid
        elif pname is not None:
            return "kill `pidof %s`" % pname
        return "echo cannot kill process because of invalid or missing pid"
