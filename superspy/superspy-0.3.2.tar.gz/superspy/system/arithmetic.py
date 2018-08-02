"""Basic arithmetic/math functions within the superspy language.
"""

from superspy import ast, language


@language.register_operator('*')
class Multiplication(ast.Operation):
    """Multiply two numbers.
    """

    priority = ast.OrderOfOperations.MULTIPLICATION

    def execute(self) -> float:
        """Execute the multiplication.

        Returns:
            float: The product.
        """
        return self.left.execute() * self.right.execute()

    def __repr__(self) -> str:
        return f'MULTIPLICATION ({repr(self.left)}) TIMES ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}MULTIPLICATION\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}*\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_operator('/')
class Division(ast.Operation):
    """Divide two numbers.
    """

    priority = ast.OrderOfOperations.MULTIPLICATION

    def execute(self) -> float:
        """Execute the Division.

        Returns:
            float: The ratio.
        """
        return self.left.execute() / self.right.execute()

    def __repr__(self) -> str:
        return f'DIVISION ({repr(self.left)}) OVER ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}DIVISION\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}/\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_operator('+')
class Addition(ast.Operation):
    """Add two numbers.
    """

    priority = ast.OrderOfOperations.ADDITION

    def execute(self) -> float:
        """Executes the addition.

        Returns:
            float: The sum.
        """
        return self.left.execute() + self.right.execute()

    def __repr__(self) -> str:
        return f'ADDITION ({repr(self.left)}) PLUS ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}ADDITION\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}+\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_operator('-')
class Subtraction(ast.Operation):
    """Subtract two numbers.
    """

    priority = ast.OrderOfOperations.ADDITION

    def execute(self) -> float:
        """Executes the subtraction.

        Returns:
            float: The dfference.
        """
        return self.left.execute() - self.right.execute()

    def __repr__(self) -> str:
        return f'SUBTRACTION ({repr(self.left)}) MINUS ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}DIFFERENCE\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}-\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_operator('==')
class Equivalence(ast.Operation):
    """Checks for equivalence of two values.
    """

    priority = ast.OrderOfOperations.EQUAL_COMPARISON

    def execute(self) -> bool:
        """Executes the comparison.

        Returns:
            bool: The equivalence.
        """
        return self.left.execute() == self.right.execute()

    def __repr__(self) -> str:
        return f'EQUIVALENCE ({repr(self.left)}) EQUALS ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}EQUIVALENCE\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}==\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_operator('!=')
class UnEquivalence(ast.Operation):
    """Checks for unequivalence (!=) of to values.
    """

    priority = ast.OrderOfOperations.EQUAL_COMPARISON

    def execute(self) -> bool:
        """Executes the comparison.

        Returns:
            bool: The unequivalence.
        """
        return self.left.execute() != self.right.execute()

    def __repr__(self) -> str:
        return f'UNEQUIVALENCE ({repr(self.left)}) IS NOT ({repr(self.right)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}UNEQUIVALENCE\n'\
            f'{self.left.deep_repr(indent+self.addint)}\n'\
            f'{indent+self.addint}!=\n'\
            f'{self.right.deep_repr(indent+self.addint)}'


@language.register_function('not')
class Not(ast.Function):
    """Invertes a value.
    This also works for non boolean value as it will check for truthyness and
    invert that.
    """

    priority = ast.OrderOfOperations.EXPRESSION

    def execute(self) -> bool:
        """Execute the operation.

        Returns:
            bool: Not the input value.
        """
        return '0' if self.argument.executes_as_true() else '1'

    def __repr__(self) -> str:
        return f'NOT ({self.args[0]})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}NOT\n{self.args[0].deep_repr(indent+self.addint)}'
