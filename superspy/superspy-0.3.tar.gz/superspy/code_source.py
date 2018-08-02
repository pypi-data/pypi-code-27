"""Code Sources provide lines for the code.

The responsibility of a code source to provide an abstract syntax tree with
new lines while parsing and/or interpreting.
"""

from abc import ABC
from typing import List


class CodeSource(ABC):
    """This is the an abstract code source base.

    It has to be inherited from, but already provides a mechanism, that, if not
    overwritten will feed all of it's lines, in the code variable to the
    abstract syntax tree.

    Attributes:
        code (List[str]): A list of lines, each a string. Does not have to be
            used by an inheriting class, but provides the auto-feed-mechanism.
            Each line should end in `\n`.
        execution_index (int): The current index in the code variable that has
            to be returned next.
    """

    code: List[str] = ''
    execution_index: int = 0

    # pylint: disable=unused-argument
    # because is_valid is unused in this case, but supposed to be usable by
    # inheriting classes
    def next_line(self, is_valid: bool) -> str:
        """Return the next line.

        This method gets called when the abstract syntax tree requires another
        line of code.

        Args:
            is_valid (bool): Is the syntax tree currently valid. Used to
                provide an indent in the ShellSource. For example.
                Not used by the default CodeSource.

        Returns:
            str: The next line.
        """
        line = self.code[self.execution_index]
        self.execution_index += 1
        return line

    def has_more_lines(self) -> bool:
        """Does this code source have any more lines.

        Returns:
            bool: The return value. True if the code source can still provide
                more lines. False if it reached the end of it's source. The
                shell still returns True, even if it does not have any more
                lines ready to be returned, because it wants the abstract
                syntax tree to query for more lines.
        """
        return self.execution_index != len(self.code)


class StringSource(CodeSource):
    """A code source that takes its entire script from a string.
    """

    def __init__(self, code: str):
        """Initialize the code source and pass it its code string.

        Args:
            code (str): The string that the code source runs from.
        """
        self.code = [f'{line}\n' for line in code.split('\n')]


class FileSource(StringSource):
    """A code source that takes its entire script from a file.
    """

    def __init__(self, filename: str):
        """Initialize the code source and pass it its file.

        Args:
            filename (str): The name of the script (relative to the main
            Python script) to be executed
        """
        with open(filename, 'r') as f:
            super().__init__(f.read())


class ShellSource(CodeSource):
    """A code source that takes its script from an interactive shell using
    `input()`.

    Attributes:
        prompt (str): The prompt to be displayed at the front of each line in
            the shell. Should end if a space.
    """

    prompt = '[🕵] '

    def next_line(self, is_valid: bool) -> str:
        """Return the next line.

        Retrieved from `input()`. If the current abstract syntax tree is not
        valid it assumes that there currently is an unused closing brace and
        thus indents the line.

        Args:
            is_valid (bool): Is the syntax tree currently valid. Used to
                provide an indent.

        Returns:
            str: The next line.
        """
        indent = '' if is_valid else '    '
        return input(f'{self.prompt}{indent}')

    def has_more_lines(self) -> bool:
        """Does this code source have any more lines.

        Returns:
            bool: Always True, as the shell will always prompt for more lines
                unless the syntax tree interpreter terminates, at which point
                it will stop asking for lines.
        """
        return True
