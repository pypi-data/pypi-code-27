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

from os import symlink, getcwd

from buildok.action import Action


class MakeSymlink(Action):
    r"""Make a symlink for a target source.

    Args:
        src (str): Source of files.
        dst (str): Target destination of symlink.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `src` or `dst` is provided or if `dst` already exists.

    Accepted statements:
        ^create symlink from `(?P<src>.+)` to `(?P<dst>.+)`$
        ^make symlink `(?P<dst>.+)` from `(?P<src>.+)`$
        ^make symlink `(?P<dst>.+)`$

    Sample input:
        - Run `touch buildok_test_symlink`.
        - Make symlink `buildok_test_symlink_ok` from `buildok_test_symlink`.

    Expected:
        Created symlink buildok_test_symlink => buildok_test_symlink_ok
    """

    def run(self, src=None, dst=None, *args, **kwargs):
        if src is None:
            src = getcwd()
        try:
            symlink(src, dst)
            self.success("Created symlink %s => %s" % (src, dst))
        except OSError as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, src=None, dst=None, *args, **kwargs):
        if src is None and dst is None:
            return "echo invalid ln command"
        elif src is None:
            src = "."
        elif dst is None:
            dst = "."
        return "ln -s %s %s" % (src, dst)
