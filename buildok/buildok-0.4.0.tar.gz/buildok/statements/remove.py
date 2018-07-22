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

from os import path, remove
from shutil import rmtree

from buildok.action import Action


class Remove(Action):
    r"""Remove files from a given source.

    Args:
        src (str): Source of files.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `src` is provided.

    Accepted statements:
        ^remove from `(?P<src>.+)`$
        ^remove `(?P<src>.+)` files$
        ^remove (?:file|folder|directory) `(?P<src>.+)`$

    Sample input:
        - Go to `/tmp`.
        - Run `touch buildok_test_tmp.txt`.
        - Remove file `buildok_test_tmp.txt`.

    Expected:
        Removed => buildok_test_tmp.txt
    """

    def run(self, src=None, *args, **kwargs):
        try:
            if path.isfile(src):
                remove(src)
            elif path.isdir(src):
                rmtree(src)
            self.success("Removed => %s" % src)
        except OSError as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, src=None, *args, **kwargs):
        flags = kwargs.get("flags", "")
        if src is None:
            src = "."
        if path.isdir(src):
            flags = " -r"
        if flags == "":
            flags = " -f"
        else:
            flags += "f"
        return "rm%s %s 2> /dev/null" % (flags, src)
