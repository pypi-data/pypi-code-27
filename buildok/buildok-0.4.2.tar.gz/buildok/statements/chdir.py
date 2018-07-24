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

from os import chdir

from buildok.action import Action


class ChangeDir(Action):
    r"""Change current working directory.

    Args:
        path (str): Path to new working directory.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `path` is provided.

    Accepted statements:
        ^go to `(?P<path>.+)`$
        ^change (?:dir|directory|folder) to `(?P<path>.+)`$

    Sample input:
        - Go to `/tmp`.

    Expected:
        Changed directory => /tmp
    """

    def run(self, path=None, *args, **kwargs):
        if path is None:
            path = "."
        try:
            chdir(path)
            self.success("Changed directory => %s" % path)
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, path=None, *args, **kwargs):
        if path is None:
            path = "."
        return "cd %s" % path
