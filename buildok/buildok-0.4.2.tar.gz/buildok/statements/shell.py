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

from shlex import split as cmd_split
from subprocess import check_output, CalledProcessError, STDOUT

from buildok.action import Action


class ShellExec(Action):
    r"""Run a command in shell.

    Args:
        cmd (str): Raw shell command.

    Retuns:
        str: Output as string.

    Raises:
        OSError: If an invalid `cmd` is provided.

    Accepted statements:
        ^run `(?P<cmd>.+)`$

    Sample input:
        - Run `echo hello friend how are you`.

    Expected:
        Output => hello friend how are you
    """

    def run(self, cmd=None, *args, **kwargs):
        safe_cmd = cmd_split(cmd)
        output_args = {"stderr": STDOUT}
        if self.env.shell_args is not None:
            if self.env.shell_args.unsafe_shell:
                output_args.update({"shell": True})
            else:
                cmd = safe_cmd
        try:
            output = check_output(cmd, **output_args)
            if output is None:
                output = "n/a"
            self.success(u"Output => %s" % output.decode('utf-8').strip())
        except CalledProcessError as e:
            self.fail(e.output)
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, cmd=None, *args, **kwargs):
        if cmd is None:
            return "echo Invalid script or missing cmd"
        return cmd
