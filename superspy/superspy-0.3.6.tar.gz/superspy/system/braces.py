"""Basic braces for the superspy language for non flat code.
"""

from typing import List

from superspy import ast, language


@language.register_single_character_touching_token('{')
class OpenBrace(ast.Token):
    """An open brace (`{`) token.
    """
    pass


@language.register_single_character_touching_token('}')
class ClosingBrace(ast.Token):
    """A closing brace (`}`) token.
    """
    pass


@language.register_command
class Group(ast.Command):
    """A group or closure which contains multiple lines of code.
    It groups multiple lines of code into one command, which can be used by
    flow control commands like `if` or `while`.

    Attributes:
        commands (List[ast.Command]): The list of commands inside the group.
        sub_ast (ast.SubAst): The sub ast managing the parsing and interpreting
            of the group.
    """

    commands: List[ast.Command]
    priority = ast.OrderOfOperations.BRACES
    sub_ast: ast.SubAst

    def __init__(self,
                 _ob: OpenBrace,
                 commands: List[ast.Token],
                 _cb: ClosingBrace):
        """Initialize and set up the group

        Args:
            _ob (OpenBrace): The opening brace.
            commands (List[ast.Token]): The commands inside the group.
            _cb (ClosingBrace): The clsing brace.
        """
        super().__init__()
        self.commands = commands

    def execute(self):
        """Interprete the group.
        """
        self.sub_ast.interpret()
        self.sub_ast.execution_index = 0

    def namespace(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return f'{super().namespace()}/GROUP@{self.line_number}'

    def build_token_tree(self):
        """Build the token tree inside the group.
        This is necessary since the group might be created during the parsing
        of the main ast and the commands might not be completeley transformed
        into the final token tree.
        """
        if not self.has_built_token_tree:
            self.has_built_token_tree = True
            self.sub_ast = ast.SubAst(self.ast)
            self.sub_ast.ast = self.commands
            self.sub_ast.build_token_tree()

    def __repr__(self) -> str:
        return f'GROUP {self.line_number}: '\
            f'{" ".join(repr(command) for command in self.commands)}\n'

    def deep_repr(self, indent='') -> str:
        command_string = "".join(command.deep_repr(indent+self.addint)
                                 for command in self.commands)
        return f'{indent}GROUP[{self.line_number}]\n{command_string}\n'
