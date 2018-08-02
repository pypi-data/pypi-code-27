"""Basic flow control functions within the superspy language.
"""

from typing import Optional

from superspy import ast, language
from superspy.system import base_language


@language.register_token('if')
class IfToken(ast.Token):
    """An `if` token.
    """
    pass

@language.register_token('else')
class ElseToken(ast.Token):
    """An `else` token.
    """
    pass


@language.register_falsy_value(0)
@language.register_falsy_value(0.0)
@language.register_falsy_value('0')
@language.register_command
class IfCondition(ast.Command):
    """A simple if condition without an else case.

    Attributes:
        condition (ast.Command): The condition determining the execution.
        group (ast.Command): The code to be executed if the condition holds.
    """

    priority = ast.OrderOfOperations.FLOW_CONTROL

    condition: ast.Command
    group: ast.Command

    def __init__(self,
                 _iftoken: IfToken,
                 condition: ast.Command,
                 _newline: Optional[base_language.NewLine],
                 group: ast.Command):
        """Initialize the if condition.

        Args:
            _iftoken (IfToken): The `if` token.
            condition (ast.Command): The condition determining the execution.
            _newline (Optional[base_language.NewLine]): An optional newline
                character after the condition before the opening brace or other
                command to be executed.
            group (ast.Command): The code to be executed if the condition
                holds true.
        """
        super().__init__()
        self.condition = condition
        self.group = group

    def execute(self):
        """Execute the statement, its condition, and possibly its group.
        """
        if self.ast.runtime.language.evaluates_as_true(
                self.condition.execute()):
            self.group.execute()

    def __repr__(self) -> str:
        return f'CONDITION ({repr(self.condition)}) '\
            f'IF TRUE ({repr(self.group)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}CONDITION\n'\
            f'{self.condition.deep_repr(indent+self.addint)}\n'\
            f'{indent}IF TRUE\n'\
            f'{self.group.deep_repr(indent + self.addint)}'


@language.register_command
class IfElseCondition(ast.Command):
    """A simple if condition with an else case.

    Attributes:
        condition (ast.Command): The condition determining the execution.
        group_true (ast.Command): The code to be executed if the condition
            yields True.
        group_false (ast.Command): The code to be executed if the condition
            yields False.
    """

    priority = ast.OrderOfOperations.FLOW_CONTROL - 0.1

    condition: ast.Command
    group_true: ast.Command
    group_false: ast.Command

    def __init__(self, _iftoken: IfToken,
                 condition: ast.Command,
                 _newline1: Optional[base_language.NewLine],
                 group_true: ast.Command,
                 _newline2: Optional[base_language.NewLine],
                 _elsetoken: ElseToken,
                 _newline3: Optional[base_language.NewLine],
                 group_false: ast.Command):
        """Initialize the if/else condition.

        Args:
            _iftoken (IfToken): The `if` token.
            condition (ast.Command): The codition determining the execution.
            _newline1 (Optional[base_language.NewLine]): An optional newline.
            group_true (ast.Command): The code to be executed if the condition
                yields True.
            _newline2 (Optional[base_language.NewLine]): An optional newline.
            _elsetoken (ElseToken): The `else` token.
            _newline3 (Optional[base_language.NewLine]): An optional newline.
            group_false (ast.Command): The code to be executed if the condition
                yields False.
        """
        super().__init__()
        self.condition = condition
        self.group_true = group_true
        self.group_false = group_false

    def execute(self):
        """Execute the statement by executing its condtion and then one group.
        """
        if self.ast.runtime.language.evaluates_as_true(
                self.condition.execute()):
            self.group_true.execute()
        else:
            self.group_false.execute()

    def __repr__(self) -> str:
        return f'CONDITION ({repr(self.condition)}) '\
            f'IF TRUE ({repr(self.group_true)}) '\
            f'IF FALSE ({repr(self.group_false)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}CONDITION\n'\
            f'{self.condition.deep_repr(indent+self.addint)}\n'\
            f'{indent}IF TRUE\n'\
            f'{self.group_true.deep_repr(indent + self.addint)}\n'\
            f'{indent}IF FALSE\n'\
            f'{self.group_false.deep_repr(indent + self.addint)}'


@language.register_token('while')
class WhileToken(ast.Token):
    """A `while` token.
    """
    pass


@language.register_command
class WhileLoop(ast.Command):
    """A while loop repeatedly executing a command while a condition is True.

    Attributes:
        condition (ast.Command): The codition determining the execution.
        group (ast.Command): The group to execute.
    """

    priority = ast.OrderOfOperations.FLOW_CONTROL

    condition: ast.Command
    group: ast.Command

    def __init__(self,
                 _whiletoken: WhileToken,
                 condition: ast.Command,
                 _newline: Optional[base_language.NewLine],
                 group: ast.Command):
        """Initialize the while loop.

        Args:
            _whiletoken (WhileToken): The `while` token.
            condition (ast.Command): The condition determining the execution.
            _newline (Optional[base_language.NewLine]): An optional newline.
            group (ast.Command): The group to execute while the condition is
                True.
        """
        super().__init__()
        self.group = group
        self.condition = condition

    def execute(self):
        """Check the condition and the running state of the ast for running.
        """
        while self.condition.executes_as_true() and self.ast.is_running():
            self.group.execute()

    def __repr__(self) -> str:
        return f'LOOP WHILE ({repr(self.condition)}): ({repr(self.group)})'

    def deep_repr(self, indent='') -> str:
        return f'{indent}LOOP WHILE\n'\
            f'{self.condition.deep_repr(indent+self.addint)}\n'\
            f'{self.group.deep_repr(indent + self.addint)}'


@language.register_token('exit')
class ExitToken(ast.Token):
    """An `exit` token.
    """
    pass


@language.register_command
class Exit(ast.Command):
    """Exit the program with an optional exit code.

    Attributes:
        exit_code (ast.Command): The exit code to end with.
    """

    priority = ast.OrderOfOperations.EXPRESSION

    exit_code: Optional[ast.Command]

    def __init__(self, _exittoken: ExitToken,
                 exit_code: Optional[ast.Command]):
        """Summary

        Args:
            _exittoken (ExitToken): The exit token.
            exit_code (Optional[ast.Command]): An optional exit code.
        """
        super().__init__()
        self.exit_code = exit_code

    def execute(self):
        """Set the exit code of the ast depending on the argument.
        """
        exit_code = 0
        if self.exit_code is not None:
            exit_code = self.exit_code.execute()
        self.ast.runtime.exit_code = exit_code

    def __repr__(self) -> str:
        if self.exit_code is not None:
            return f'EXIT ({repr(self.exit_code)})'
        return f'EXIT'

    def deep_repr(self, indent='') -> str:
        if self.exit_code is not None:
            return f'{indent}EXIT\n'\
            f'{self.exit_code.deep_repr(self.addint + indent)}'
        return f'{indent}EXIT'
