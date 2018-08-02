"""Manage the setting of variables in the superspy language.
"""

from superspy import ast, language


@language.register_token('=')
class SetSymbol(ast.Token):
    """A `=` token.
    """
    pass


@language.register_command
class SetVariable(ast.Command):
    """Set a variable.

    Attributes:
        value (ast.Command): The value to set the variable to.
        variable (ast.Variable): The variable to set.
    """

    priority = ast.OrderOfOperations.ASSIGNMENT

    variable: ast.Variable
    value: ast.Command

    def __init__(self,
                 variable: ast.Variable,
                 _set_symbol: SetSymbol,
                 value: ast.Command):
        """Initialize the set command.

        Args:
            variable (ast.Variable): The variable to set.
            _set_symbol (SetSymbol): The `=` token.
            value (ast.Command): The value to set the variable to.
        """
        super().__init__()
        self.variable = variable
        self.value = value

    def execute(self):
        """Execute the value and set the variable to it.
        """
        self.variable.set(self.value.execute())

    def __repr__(self) -> str:
        return f'SET {self.variable.content} TO ({repr(self.value)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}SET\n'\
            f'{self.variable.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}=\n'\
            f'{self.value.deep_repr(indent+self.addint)}'
