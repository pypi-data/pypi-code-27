"""Basic language structure for the superspy language.
"""

from typing import Any

from superspy import ast, language

# Delimit words with spaces
@language.register_word_delimiter(' ')
# Delimit commands with semicolons and newlines
@language.register_single_character_touching_token(';')
@language.register_single_character_touching_token('\n')
class NewLine(ast.Token):
    """Newline token.
    """
    def deep_repr(self, indent='') -> str:
        return super().deep_repr(indent) + '\n'


@language.register_command
class Line(ast.Command):
    """A line containing a single command.

    Attributes:
        command (ast.Command): The command making up the line.
    """

    command: ast.Command
    priority = ast.OrderOfOperations.COMMA
    can_contain_self = False

    def __init__(self, command: ast.Command, _: NewLine):
        """Initialize a line object.

        Args:
            command (ast.Command): The command.
            _ (NewLine): The new line character token.
        """
        super().__init__()
        self.command = command

    def execute(self) -> Any:
        """Execute the line by executing its single command.

        Returns:
            Any: The return value of the command.
        """
        return self.command.execute()

    def get_trace(self):
        return f'LINE {self.line_number}'

    def __repr__(self) -> str:
        return f'LINE {self.line_number}: {repr(self.command)}\n'

    def deep_repr(self, indent='') -> str:
        return f'{indent}LINE[{self.line_number}]\n'\
            f'{self.command.deep_repr(indent+self.addint)}\n'


@language.register_command
class EmptyLine(ast.Command):
    """An empty line not containing any command.
    This is needed to, after all other lines have matched match the remaining
    newline tokens.
    """

    priority = ast.OrderOfOperations.COMMA + 0.1

    def __init__(self, _: NewLine):
        """Initialize the empty line.

        Args:
            _ (NewLine): The new line character token.
        """
        super().__init__()

    def execute(self):
        """Execute an empty line - do nothing.
        """
        pass

    def __repr__(self) -> str:
        return f'LINE {self.line_number}: EMPTY\n'

    def deep_repr(self, indent='') -> str:
        return f'{indent}LINE[{self.line_number}]: EMPTY\n'
