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

from shutil import move

from buildok.action import Action


class Move(Action):
    r"""Move files from a given source to a given destination.

    Args:
        src (str): Source of files.
        dst (str): Target destination of files.

    Retuns:
        str: Status of move.

    Raises:
        OSError: If an invalid `src` or `dst` is provided.

    Accepted statements:
        ^move from `(?P<src>.+)` to `(?P<dst>.+)`$
        ^move `(?P<src>.+)` files to `(?P<dst>.+)`$
        ^rename `(?P<src>.+)` to `(?P<dst>.+)`$

    Sample input:
        - Go to `/tmp`.
        - Create folder `buildok_test_folder_move`.
        - Rename `buildok_test_folder_move` to `buildok_test_folder_moved`.

    Expected:
        Moved buildok_test_folder_move => buildok_test_folder_moved
    """

    def run(self, src=None, dst=None, *args, **kwargs):
        try:
            move(src, dst)
            self.success("Moved %s => %s" % (src, dst))
        except OSError as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, src=None, dst=None, *args, **kwargs):
        if src is None and dst is None:
            return "echo invalid move command"
        elif src is None:
            src = "."
        elif dst is None:
            dst = "."
        return "mv %s %s" % (src, dst)
