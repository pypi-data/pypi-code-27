"""Summary
"""

from superspy import ast, language


@language.register_token('getnum')
class GetNum(ast.Command):
    """Get a number from user input.
    """

    def execute(self) -> float:
        """Ask for input and convert it to a float.

        Returns:
            float: The user input.
        """
        return float(input())

    def __repr__(self) -> str:
        return f'GET NUMBER'

    def deep_repr(self, indent='') -> str:
        return f'{indent}GET NUMBER'


@language.register_token('getstr')
class GetStr(ast.Command):
    """Get a string from user input.
    """

    def execute(self) -> str:
        """Ask for input.

        Returns:
            str: The input.
        """
        return input()

    def __repr__(self) -> str:
        return f'GET STRING'

    def deep_repr(self, indent='') -> str:
        return f'{indent}GET STRING'


@language.register_function('print', 1)
class Print(ast.Function):
    """Print a given argument.
    """

    def execute(self):
        """Execute the argument and print it.
        """
        print(self.argument.execute())

    def __repr__(self) -> str:
        return f'PRINT ({self.argument})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}PRINT\n{self.argument.deep_repr(indent+self.addint)}'


@language.register_function('printnl', 1)
class PrintNL(ast.Function):
    """Print a given argument without a newline (No Line).
    """

    def execute(self):
        """Execute the argument and print it.
        """
        print(self.argument.execute(), end='')

    def __repr__(self) -> str:
        return f'PRINTNL ({self.argument})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}PRINTNL\n'\
            f'{self.argument.deep_repr(indent+self.addint)}'


@language.register_token('dis')
class Disassemble(ast.Command):
    """Print the token tree built by the ast.
    """

    def execute(self):
        """Call the corresponding function in the ast.
        """
        print(self.ast.runtime.root_ast.deep_repr())

    def __repr__(self) -> str:
        return f'DISASSEMBLE'

    def deep_repr(self, indent='') -> str:
        return f'{indent}DISASSEMBLE'
