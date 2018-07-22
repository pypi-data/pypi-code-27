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

from os import path

from buildok.util.log import Log
from buildok.util.console import Console


class Reader(object):
    """Reader wrapper to gather build steps.

    Attributes:
        READER (str): Class extending Reader.
        PATH   (str): Path to build steps file.

    Args:
        validate (bool): Enable or disable build steps validation.
        filename  (str): Build filename.
        content  (list): Content from file context.
        cursor    (int): Current line index being scanned.
        line      (str): Current line content.
    """

    READER, PATH = None, r"."

    def __init__(self, validate=False):
        self.validate = validate
        self.filename = ""
        self.content, self.cursor, self.line = [], 0, ""
        self.setup() or self.crash()

    @classmethod
    def set_project_path(cls, project_path):
        """Change project path.

        Default is current working directory.

        Args:
            project_path (str): New project path.

        Raises:
            ValueError: If project path is not a string.
        """

        if not isinstance(project_path, (str, unicode)):
            Log.fatal("Project path must be string")
        cls.PATH = project_path.rstrip("/")

    def parse(self):
        """Parse build steps file.

        Raises:
            NotImplementedError: Readers must implement this method.
        """

        raise NotImplementedError("Must implement read method")

    def read(self):
        """Read build file content.

        Raises:
            OSError: If `filename` cannot be found or accesed.
        """

        with open(self.filename, "rb") as file_:
            self.content = [r.rstrip("\n") for r in file_.readlines()]

    def exists(self):
        """Check if build file exists.

        Returns:
            bool: Returns True if `filename` exists, otherwise False.
        """

        return path.isfile(self.filename)

    def crash(self):
        """Crash reader with an error.

        Raises:
            NotImplementedError: Reader must overwrite READER attribute.
        """

        raise NotImplementedError("Directly call on Reader not allowed")

    def setup(self):
        """Setup if reader is properly called.

        Raises:
            ValueError: Project does not have build file.

        Returns:
            bool: Returns True if project setup is done.
        """

        if self.READER is None or self.PATH is None:
            return False
        filepath = self.PATH
        if path.isdir(filepath):
            filepath = path.join(self.PATH, self.READER)
        self.filename = path.abspath(filepath)
        if not self.exists():
            Log.fatal("Project does not have a proper build file: %s" % filepath)
        return True

    def get_build_source(self):
        """Get a tuple of build file and a validation flag.

        Returns:
            build_file (str): Build file.
            validate  (bool): True if has to be validated.
        """

        return (self.filename, self.validate)

    def has_next(self):
        """Check if reader has more lines to read.

        Returns:
            bool: True if it has unread lines, otherwise False.
        """

        more_lines = len(self.content) > self.cursor
        if more_lines:
            self.line = self.content[self.cursor]
        return more_lines

    def get_line(self, strip=False):
        """Get current line read.

        Args:
            strip (bool): Strips text of whitespace if True.

        Returns:
            str: Current line from build file.
        """

        return self.line.strip() if strip else self.line

    def get_line_number(self):
        """Get current line number.

        Returns:
            int: Current line number from build file.
        """

        return self.cursor

    def next_line(self):
        """Go to next line in build file.

        It actually calls skip_line() with 1 iteration.
        """

        self.skip_line()

    def skip_line(self, lines=1):
        """Jump X lines ahead in build file.

        Move line cursor ahead. By default it jumps one line.
        Can go backwards if negative number is provided.
        """

        self.cursor += lines

    def next_content(self):
        """Get content ahead of cursor.

        Returns:
            list (list): Returns content ahead of cursor or empty list.
        """

        index = self.cursor + 1
        if index >= len(self.content):
            return []
        return self.content[index:]

    def preview(self, limit=80):
        """Preview build file.

        Outputs list of all lines from build file with line number in front.
        """

        self.read()
        max_line = len(str(len(self.content))) + 1
        limit -= max_line
        print()
        for i, line in enumerate(self.content):
            _line = line
            preview_line = ""
            prefix = ("%" + str(max_line) + "d |") % (i + 1)
            if len(line) == 0:
                preview_line = prefix + " [newline]"
            while len(line) > 0:
                preview_line += "%s %s\n" % (prefix, line[:limit])
                line = line[limit:]
            print(self.preview_line(_line, preview_line.rstrip("\n")))
        print()

    def preview_line(self, line, preview_line):
        """Preview line from build file.

        Useful to customize the display row of a line.
        """

        return Console.darkgray(preview_line)
