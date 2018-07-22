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

from __future__ import print_function

from stat import S_ISREG, S_ISFIFO, S_ISSOCK, S_ISLNK, S_ISDIR, S_ISCHR, S_ISBLK
from os import listdir, stat, getcwd, path as fpath

from buildok.action import Action


class ListDir(Action):
    r"""List files in directory.

    Args:
        path (str): Path to directory.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        OSError: If an invalid `path` is provided.

    Accepted statements:
        ^list (?:files|folders) (?:in|from|of) `(?P<path>.+)`$
        ^list everything$

    Sample input:
        - List files in `/tmp`.

    Expected:
        Listing directory => /tmp
    """

    def run(self, path=None, *args, **kwargs):
        if path is None:
            path = getcwd()
        length = 80
        try:
            content = listdir(path)
            fullpath = fpath.abspath(path)
            self.success("Listing directory => %s" % fullpath)
            print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
            s_name = int((length-7) * .8)
            s_size = int((length-7) - s_name)
            print(u"\033[90m|   |\033[0m %-{}s\033[90m|\033[0m %-{}s\033[90m|\033[0m".format(s_name, s_size) % ("Name", "Size"))
            print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
            for f in content:
                f_name = f if len(f) <= s_name else f[:s_name-3] + "..."
                f_type = self.get_file_type(fullpath, f)
                f_size = self.get_file_size(fullpath, f) if f_type == "f" else "--"
                print(u"\033[90m| %s |\033[0m %-{}s\033[90m|\033[0m %-{}s\033[90m|\033[0m".format(s_name, s_size) % (f_type, f_name, f_size))
            print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
        except Exception as e:
            self.fail(str(e))

    def get_file_size(self, root, filename):
        filepath = fpath.join(root, filename)
        return ListDir.sizeof_fmt(fpath.getsize(filepath))

    def get_file_type(self, root, filename):
        filepath = fpath.join(root, filename)
        filemode = stat(filepath).st_mode
        if S_ISREG(filemode):
            return "f"
        elif S_ISSOCK(filemode):
            return "s"
        elif S_ISFIFO(filemode):
            return "p"
        elif S_ISLNK(filemode):
            return "l"
        elif S_ISDIR(filemode):
            return "d"
        elif S_ISCHR(filemode):
            return "c"
        elif S_ISBLK(filemode):
            return "b"
        return "?"

    @classmethod
    def convert_shell(cls, path=None, *args, **kwargs):
        if path is None:
            path = "."
        return "ls -hal %s" % path

    @staticmethod
    def sizeof_fmt(num):
        # https://web.archive.org/web/20111010015624/http://blogmag.net/blog/read/38/Print_human_readable_file_size
        for x in ["bytes", "KB", "MB", "GB", "TB"]:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return num
