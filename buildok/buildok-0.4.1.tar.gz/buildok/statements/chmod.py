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

from os import chmod, getcwd, path as fpath

from buildok.action import Action


class ChangeMod(Action):
    r"""Change permissions on file or directory.

    Args:
        mode (str): Octal integer permissions.
        path (str): Path to file or directory.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `path` is provided.
        TypeError: If an invalid `mode` is provided.

    Accepted statements:
        ^change permissions to `(?P<mode>.+)`$
        ^change permissions to `(?P<mode>.+)` for `(?P<path>.+)`$
        ^change permissions `(?P<mode>.+)` for `(?P<path>.+)`$
        ^set permissions (?:to )?`(?P<mode>.+)` (?:for|to|on) `(?P<path>.+)`$

    Sample input:
        - Run `touch /tmp/buildok_test.txt`.
        - Set permissions to `400` for `/tmp/buildok_test.txt`.

    Expected:
        Changed permissions 400 => /tmp/buildok_test.txt
    """

    def run(self, mode="400", path=None, *args, **kwargs):
        if path is None:
            path = getcwd()
        try:
            chmod(path, int(mode, 8))
            self.success("Changed permissions %s => %s" % (mode, path))
        except OSError as e:
            self.fail(str(e))
        except TypeError as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, mode="400", path=None, *args, **kwargs):
        if path is None:
            path = "."
        flags = kwargs.get("flags", "")
        if fpath.isdir(path):
            flags = " -R"
        return "chmod%s %s %s" % (flags, mode, path)
