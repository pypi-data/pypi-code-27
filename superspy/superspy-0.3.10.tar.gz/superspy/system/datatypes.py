"""Basic datatypes for the superspy language.
"""

from superspy import ast, language


@language.register_data_type(r'^(\d*\.)?\d+$')
class Number(ast.DataType):
    """A number that takes floats and ints and stores them as float.
    """

    def __init__(self, line_number: int, content: str):
        """Initialize and set up the number from a string from the tree.
        """
        super().__init__(line_number, content)
        self.value = float(content)


@language.register_literality_delimiter('"', '"')
@language.register_data_type(r'^".*"$')
class String(ast.DataType):
    """A string.
    """

    def __init__(self, line_number: int, content: str):
        """Initialize and set up the string from the tree.
        """
        super().__init__(line_number, content)
        self.value = content[1:-1]
