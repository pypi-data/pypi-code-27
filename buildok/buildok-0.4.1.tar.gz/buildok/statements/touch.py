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

from buildok.action import Action


class Touch(Action):
    r"""Create a new file.

    Args:
        filepath (str): Full path of the file.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `filepath` is provided.

    Accepted statements:
        ^create(?: new)? file `(?P<filepath>[\w\.]+)`$

    Sample input:
        - Create file `/tmp/buildok.txt`.

    Expected:
        Created file => /tmp/buildok.txt
    """

    def run(self, filepath=None, *args, **kwargs):
        try:
            with open(filepath, "w") as file_:
                file_.write("")
            self.success("Created file => %s" % filepath)
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, filepath=None, *args, **kwargs):
        if filepath is None:
            return "echo invalid touch call"
        return "touch %s" % filepath
