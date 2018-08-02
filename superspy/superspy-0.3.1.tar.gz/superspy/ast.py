"""This is the core of superspy; it handles most of the parsing and execution.
"""

import re
from abc import ABC, abstractmethod

from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from superspy import code_source, language


# pylint: disable=too-few-public-methods
# This class is not supposed to have methods, it is a bit like an enum.
class OrderOfOperations:
    """Order of operations priorities reference.
    They are floats, so values in-between can be chosen if so desired.
    The default library limits itself to those values, some commands are
    + or - 0.1 if they need to be parsed before or after a specific other
    command.

    Adapted from Wikipedia: https://en.wikipedia.org/wiki/Order_of_operations
    """
    FUNCTION_CALL = 1.0
    UNARY = 2.0
    MULTIPLICATION = 3.0
    ADDITION = 4.0
    BIT_SHIFT = 5.0
    UNEQUAL_COMPARISON = 6.0
    EQUAL_COMPARISON = 7.0
    AND_BW = 8.0
    XOR_BW = 9.0
    OR_BW = 10.0
    AND_LOGICAL = 11.0
    OR_LOGICAL = 12.0
    TERNARY = 13.0
    ASSIGNMENT = 14.0
    EXPRESSION = 15.0
    BRACES = 16.0
    FLOW_CONTROL = 17.0
    COMMA = 18.0
    UNDEFINED = 100.0
    END = 10000.0


class ErrorMode(Enum):
    """The modes an interpreter can have handling errors.

    Attributes:
        CRASH (TYPE): Crash once an error is encountered. This is the default
            in general, but should be especially for any execution of pre-made
            code, since correct execution cannot be guaranteed once one line of
            code fails.
        PRINT (TYPE): This one prints the error, but continues execution. It is
            used in the shell, where you don't want the shell to end when you
            accidentally type a variable name wrong.
        SUPPRESS (TYPE): Ignore the error silently and continue executing the
            code. This one is not used in here anywhere, but can be used by
            you. Beware however, since this might lead to issues!
        MIRROR_PARENT (TYPE): Mirror the parent ast's error mode.
    """

    SUPPRESS = auto()
    PRINT = auto()
    CRASH = auto()
    MIRROR_PARENT = auto()


###########
# CLASSES #
###########


class Token:
    """The base class of any token in the entire project.

    Tokens can be single characters like `\n`, `*` or `(`, words like `print`,
    strings, numbers, or entire statements with multiple children, so for
    example `print 4 + 3` would in the end be a Token subclass for the print
    command, with a child being the addition, itself having the children `4`,
    `3` and `+`.

    Attributes:
        line_number (int): The line number this token ends at.
        content (str): The string content this token describes.

        ast (Ast): The AST object managing this token.

        parent (Optional[Token]): The parent object.
        children (List[Token]): The children objects.

        has_built_token_tree (bool): Has this token already built a token tree.

        addint (str): Additional indent for pretty print formatting.
    """

    line_number: int
    content: str
    ast: Optional['Ast'] = None
    addint = '  '
    parent: Optional['Token'] = None
    children: List['Token'] = []
    has_built_token_tree = False

    def __init__(self, line_number: Optional[int] = None,
                 content: Optional[str] = None):
        """Initiate the token

        Args:
            line_number (int, optional): The line number this token ends at.
            content (str, optional): The string content this token describes.
        """
        if line_number is not None:
            self.line_number = line_number
        if content is not None:
            self.content = content

    def __repr__(self) -> str:
        """String representation of this object.
        """
        return f'{type(self).__name__} '\
               f'at line {self.line_number}: {repr(self.content)}'

    def deep_repr(self, indent='') -> str:
        """A deep and indented string representation of the object.

        Args:
            indent (str, optional): The indent to add before this token.

        Returns:
            str: The string representation.
        """
        return f'{indent}{type(self).__name__}[{self.line_number}]'

    def namespace(self) -> str:
        """The namespace for this object and its children.
        So for example a variable inside a loop (like i) would have a different
        namespace than a variable outside to loop, so it cannot be accessed
        there.

        Returns:
            str: The namespace.
        """
        if self.parent is None:
            return ''
        return self.parent.namespace()

    def build_token_tree(self):
        """Build the token tree of all the children.
        This is mostly only relevant for groups like braces which still have to
        be built after being grouped.
        """
        if not self.has_built_token_tree:
            self.has_built_token_tree = True
            for child in self.children:
                child.build_token_tree()

    def get_trace(self) -> str:
        """Get's a trace for this Token which can be used in error messages.

        Returns:
            str: the trace.
        """
        if self.parent is None:
            return ''
        return f'{self.parent.get_trace()}\n{repr(self)}'

    # pylint: disable=no-self-use
    # This is a method supposed to be inherited.
    def executes_as_true(self) -> bool:
        """Is this token True or False.

        Returns:
            bool: The boolean value of this token.
        """
        return False


class UndefinedToken(Token):
    """A not defined token.
    """
    pass


class Command(Token, ABC):
    """A command that can be made up of different tokens.
    It is described by a pattern made up of keywords and arguments in any
    order. It even allows for lists.

    Attributes:
        priority (float): The priority to be parsed in. Should be derived from
            OrderOfOperations. Smaller numbers get matched first.
        pattern (List[language.PATTERN]): A pattern to be matched. Look in the
            standard library for reference.
        can_contain_self (bool): Can the command contain itself.
    """

    priority: float = OrderOfOperations.UNDEFINED
    pattern: List[language.PATTERN] = None
    can_contain_self = True

    @abstractmethod
    def execute(self) -> Any:
        """Execute this command.
        """
        pass

    def executes_as_true(self) -> bool:
        """Is the value when executing this command Truthy or Falsy.

        Returns:
            bool: The return value
        """
        return self.execute() not in self.ast.runtime.language.falsy_values

    @classmethod
    def token_matches_class(cls, token: Token, class_: Type[Token]) -> bool:
        """Does this token conform to a class.

        Args:
            token (Token): The token to match.
            class_ (Type[Token]): The class to match to.

        Returns:
            bool: The return value.
        """
        if token is None or class_ is None:
            return False
        return isinstance(token, class_)

    # pylint: disable=too-many-arguments
    # This many arguments are unfortunately required.
    @classmethod
    def match_single_token(cls,
                           token_list: List[Token],
                           pattern: Type[Token],
                           next_pattern: Type[Token],
                           is_optional: bool,
                           is_list: bool) -> int:
        """Does a single pattern match one or more tokens.

        Args:
            token_list (List[Token]): A list of tokens to be matched by the
                pattern.
            pattern (Type[Token]): The pattern the token[s] have to conform to.
            next_pattern (Type[Token]): The pattern the next token has to
                conform to. Used for optionals, which can return 0 if the next
                token matches, and lists, which will match as many tokens as
                possible until the next matches.
            is_optional (bool): Is this token optional.
            is_list (bool): Is this token a list, so it matches multiple.

        Returns:
            int: The amounts of tokens matched by this pattern. -1 means it did
                not match successfully, while 0 means it matches 0 tokens,
                which is possible with optionals.
        """

        # Amount of tokens to match.
        length = 0

        while 1:
            # Reached the end.
            if len(token_list) == length:
                if length == 0 and not is_optional:
                    length = -1
                break
            next_token = token_list[length]
            if (not cls.can_contain_self) and\
                    cls.token_matches_class(next_token, cls):
                length = -1
                break

            # Next pattern matches, which limits the match.
            if cls.token_matches_class(next_token, next_pattern) and (
                    True if is_optional else length > 0):
                break

            # Matches current pattern.
            if cls.token_matches_class(next_token, pattern):
                length += 1
            # Does not match the current pattern.
            else:
                # Optionals still are successful.
                if is_optional:
                    break
                length = -1
                break

            # Only lists match multiple tokens.
            if not is_list:
                break

        return length

    @classmethod
    def type_of_token(cls, token: language.PATTERN
                      ) -> Tuple[Type[Token], bool, bool]:
        """Returns the type of a single token.
        It strips the `List` and `Optional` attributes off and returns them as
        booleans.

        Args:
            token (language.PATTERN): The token to analyze.

        Returns:
            Tuple[
                Type[Token],: The type of the token.
                bool,       : Is the token a list.
                bool        : Is the token optional.
            ]
        """
        is_list = False
        is_optional = False

        token_type = token

        # This is a bit hacky, but origin contains information about things
        # like List or Optionality for `List[Token]` or `Optional[Token]`.
        origin = token.__origin__ if hasattr(token, '__origin__') else None
        # The arguments contains information about the type of object.
        args = token.__args__ if hasattr(token, '__args__') else None

        # Matches list.
        if origin is list:
            token_type = args[0]
            is_list = True
        if origin is Union:
            # Defines NoneType, which cannot be accessed otherwise.
            NoneType = type(None)
            # An optional is a union with NoneType.
            if NoneType in args:
                is_optional = True
                # The other argument is the type of token.
                if args[0] is NoneType:
                    token_type = args[1]
                else:
                    token_type = args[0]

        return token_type, is_list, is_optional

    @classmethod
    def match(cls, token_list: List[Token]) -> List[int]:
        """Match a list of tokens to this classes pattern.

        Args:
            token_list (List[Token]): The list of tokens to match.

        Returns:
            List[int]: The amount of tokens matched by each element of the
                pattern.
        """
        length = 0
        return_list: List[int] = []

        for pattern_index, pattern_token_class in enumerate(cls.pattern):
            current_token_type, is_list, is_optional = cls.type_of_token(
                pattern_token_class)
            next_token_type = None
            if len(cls.pattern) > pattern_index + 1:
                # Get the type of the next token if there is one.
                next_token_type, _, _ = cls.type_of_token(
                    cls.pattern[pattern_index + 1])

            # Reached the end without matching the entire pattern.
            if len(token_list) == length and not is_optional:
                return []

            new_length = cls.match_single_token(
                token_list[length:],
                current_token_type,
                next_token_type,
                is_optional,
                is_list)
            # Did not match sucessfully
            if new_length == -1:
                return []
            return_list.append(new_length)
            length += new_length

        if [element for element in return_list if element > 0]:
            # Matched not only empty optionals.
            return return_list
        return []


class Function(Command, ABC):
    """A function which is a command beginning with one keyword.

    Attributes:
        args (List[Token]): The argument tokens for this instance.
        argument (Token): The first argument. Used when there only is one.
    """

    args: List[Token] = None
    argument: Token = None
    priority: float = OrderOfOperations.EXPRESSION

    def __init__(self, _: Token, *args: List[Token]):
        """Set up from the default initializer.

        Args:
            _ (Token): The function name.
            *args (List[Token]): The arguments
        """
        super().__init__()
        self.args = args
        if args:
            self.argument = args[0]

    @abstractmethod
    def execute(self) -> Any:
        """Execute this function. Overwriting it like this is required
        by pylint.
        """
        pass


class Operation(Command, ABC):
    """An operation which has an operator in the middle (like `+`) and an
    argument on each side.

    Attributes:
        left (Command): The left parameter of the operation.
        right (Command): The right parameter of the operation.
    """

    left: Command
    right: Command

    def __init__(self, left: Command, _: Token, right: Command):
        """Set up from the default initializer.

        Args:
            left (Command): The left parameter of the operation.
            _ (Token): The operator.
            right (Command): The right parameter of the operation.
        """
        super().__init__()
        self.left = left
        self.right = right

    @abstractmethod
    def execute(self) -> Any:
        """Execute this function. Overwriting it like this is required
        by pylint.
        """
        pass


class DataType(Command, ABC):
    """A datatype / value.
    """

    value: Any

    def execute(self) -> Any:
        """Return the value.

        Returns:
            Any: The value.
        """
        return self.value

    def __repr__(self) -> str:
        return f'{type(self).__name__} {repr(self.value)}'

    def deep_repr(self, indent='') -> str:
        return f'{indent}{type(self).__name__}={repr(self.value)}'


class Variable(Command):
    """A variable that support setting and getting a value.

    Attributes:
        name (str): The name of the variable.
    """

    name: str

    def __init__(self, name: str):
        """Initialize the object and set its name

        Args:
            name (str): The name of the variable.
        """
        super().__init__()
        self.name = name

    def get(self) -> Any:
        """Get the variable's value.

        Returns:
            Any: The variable's value.
        """
        search_namespace = ''
        # Iterate through all the parent namespaces and check if a variable
        # with that name exists there somewhere.
        for namespace_component in self.namespace().split('/'):
            search_namespace = f'{search_namespace}/{namespace_component}'
            variable_name = f'{search_namespace}.{self.name}'
            # If that variable is found return it.
            if variable_name in self.ast.runtime.variables:
                return self.ast.runtime.variables[variable_name]
        # If the variable is not found throw an error.
        self.ast.error(f'Variable or function {self.name} not found.',
                       self.get_trace())
        return None

    def set(self, new_value: Any):
        """Set the variable's value.

        Args:
            new_value (Any): The variable's new value.
        """
        search_namespace = ''
        # Iterate through all the parent namespaces and check if a variable
        # with that name exists there somewhere.
        for namespace_component in self.namespace().split('/'):
            search_namespace = f'{search_namespace}/{namespace_component}'
            variable_name = f'{search_namespace}.{self.name}'
            # If the variable is found set its value.
            if variable_name in self.ast.runtime.variables:
                self.ast.runtime.variables[variable_name] = new_value
                break
        else:
            # If the variable is not found set a new one.
            self.ast.runtime.variables[
                f'{search_namespace}.{self.name}'] = new_value

    def execute(self) -> Any:
        """If the variable gets executed like a command its value is returned.

        Returns:
            Any: The variable's value.
        """
        return self.get()

    def __repr__(self) -> str:
        return f'VARIABLE {self.name}'

    def deep_repr(self, indent='') -> str:
        return f'{indent}VARIABLE {self.name}'


class Runtime:
    """Class that stores runtime data.
    It has a single instance for a running script.

    Attributes:
        root_ast (Ast): The root ast of the script.
        exit_code (optional, int): The exit code of the script.
        language (language.Language): The language of the script.
        variables (Dict[str, Any]): The variables in the script.
        functions (Dict[str, Any]): The functions in the script.
    """

    root_ast: 'Ast'
    language: language.Language
    exit_code: Optional[int] = None
    variables: Dict[str, Any] = {}
    functions: Dict[str, Any] = {}

    def __init__(self, root_ast: 'Ast'):
        """Initialize and set up the Runtime.

        Args:
            root_ast (Ast): The root ast of the script.
        """
        self.root_ast = root_ast


class Ast:
    """The Abstract Syntax Tree doing most of the heavy lifting of the parsing.
    This manages all the parsing and executing of the input.

    Attributes:
        ast (List[Token]): The actual abstract syntax tree: A list of tokens.
            This is a flat list, because any depth are the sub tokens of
            another token.
        ast_is_definitely_valid_up_to (int): When parsing the AST from a
            continuing input like a shell the AST tries to match at every line.
            However with asymmetric braces it might not yet be valid. This is
            the last point the AST is entirely valid at, so the previous part
            does not have to be parsed again.
        lang (language.Language): The language this ast is parsing, matching
            and executing.
        line_number (int): The current line number the ast is parsing at.
        error_mode (ErrorMode): What to do when an error occurs, like crash or
            continue executing.
        source (code_source.CodeSource): The code source for this ast that
            supplies new lines of code.
        execution_index (int): The index the execution is currently at. This
            has to be a nonlocal variable because the shell terminates the
            execution function between lines.
    """

    ast: List[Token] = []
    source: Optional[code_source.CodeSource] = None
    error_mode: ErrorMode = ErrorMode.CRASH

    ast_is_definitely_valid_up_to = 0
    line_number = 0

    execution_index: int = 0

    runtime: Optional[Runtime] = None

    def __init__(self, source: Optional[code_source.CodeSource] = None,
                 lang: Optional[language.Language] = None):
        """Initialize the current AST with a code source and a language.

        Args:
            source (Optional[code_source.CodeSource]): The code source this ast
                draws from.
            lang (language.Language): The language this ast matches.
        """
        self.source = source
        if self.runtime is None:
            self.runtime = Runtime(self)
            if language is not None:
                self.runtime.language = lang

    def build_token_list(self, line_count: int = None):
        """Build a flat token list from strings by the code source.
        New lines are requested, either until it reaches the end or a specified
        limit. It then parses it character by character and matches it to
        elementary tokens to build a flat token list.

        Args:
            line_count (int, optional): The amount of lines to parse. If left
                empty or `None` it will run to the end of the source.
        """
        # tree building components
        current_word = ''

        # state variables
        escape_next = False
        is_literal = False
        literality_closer: chr = ''

        def save_current_word():
            """Save the current word to the token list.
            """
            nonlocal current_word
            if current_word != '':
                match_class = UndefinedToken
                # Try to match it to existing tokens.
                for regex in self.runtime.language.regex_matchers:
                    token_class = self.runtime.language.regex_matchers[regex]
                    if re.match(regex, current_word):
                        match_class = token_class
                        break
                # Initialize a new token and set it up.
                new_token = match_class(self.line_number, current_word)
                new_token.ast = self
                # Add it to the token list.
                self.ast.append(new_token)
                # Reset the current word.
                current_word = ''

        # Repeat until end of source or for specified amount of lines.
        while self.source.has_more_lines() and (
                line_count is None or line_count):
            if line_count:
                line_count -= 1
            new_line = self.source.next_line(self.is_valid())
            self.line_number += 1
            for character in new_line:
                if escape_next:
                    current_word += character
                    escape_next = False
                elif character in self.runtime.language.escape_markers:
                    escape_next = True
                elif is_literal and character == literality_closer:
                    is_literal = False
                    current_word += character
                    literality_closer = ''
                elif is_literal:
                    current_word += character
                elif character in \
                        self.runtime.language.literality_delimiter.keys():
                    literality_closer = \
                            self.runtime.language.literality_delimiter[
                                character]
                    is_literal = True
                    current_word += character
                elif character in self.runtime.language.word_delimiters:
                    save_current_word()
                elif character in \
                        self.runtime.language.single_character_tokens:
                    save_current_word()
                    current_word += character
                    save_current_word()
                else:
                    current_word += character
            save_current_word()

    def guess_variables(self):
        """Guess that all remaining tokens are variables.
        """
        for index, token in enumerate(self.ast):
            if isinstance(token, UndefinedToken):
                # Initialize and setup new variable.
                new_var = Variable(token.content)
                new_var.line_number = token.line_number
                new_var.content = token.content
                new_var.ast = self
                self.ast[index] = new_var

    def build_token_tree(self):
        """Match patterns defined for different commands and create them.
        """
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-locals
        # This is a complex function that belongs together.
        # Spreading it out more would make it less legible.
        for order_of_operation in sorted(
                self.runtime.language.commands_by_priority.keys()):
            # Reverseley walking the list, as to correctly match nested braces
            # and multiple functions.
            current_index = len(self.ast) - 1
            while current_index + 1:
                for command in self.runtime.language.commands_by_priority[
                        order_of_operation]:
                    command.ast = self
                    match = command.match(self.ast[current_index:])
                    breaks_self_matching_rule = False
                    if match and not breaks_self_matching_rule:
                        # Amount of matched
                        match_count = sum(match)

                        remaining_matched_objects = self.ast[
                            current_index:
                            current_index + match_count]
                        flat_matched_objects = remaining_matched_objects.copy()
                        # The command arguments
                        arguments: List[Union[List[Token], Token]] = []
                        for argument_index in range(len(match)):
                            _, is_list, is_optional = command.type_of_token(
                                command.pattern[argument_index])
                            argument_count = match.pop(0)
                            if argument_count == 0 and is_optional:
                                arguments.append(None)
                            elif is_list:
                                # List arguments.
                                arguments_list_arguments: List[Token] = []
                                for _ in range(argument_count):
                                    arguments_list_arguments.append(
                                        remaining_matched_objects.pop(0))
                                arguments.append(arguments_list_arguments)
                            else:
                                # Single argument.
                                arguments.append(
                                    remaining_matched_objects.pop(0))
                        # Create new command object and set it up
                        new_object = command(*arguments)
                        new_object.line_number = arguments[0].line_number
                        new_object.ast = self
                        new_object.children = flat_matched_objects
                        new_object.content = ' '.join(
                            obj.content for obj in flat_matched_objects)
                        for matched_object in flat_matched_objects:
                            matched_object.parent = new_object
                            self.ast.remove(matched_object)
                        self.ast.insert(current_index, new_object)
                        new_object.build_token_tree()
                        # Step "back" one
                        current_index += 1
                current_index -= 1

    def is_valid(self) -> bool:
        """Is the current syntax tree valid.
        This is checked by every token being subclass of command and thus being
        executable.

        Returns:
            bool: The validity.
        """
        for i in range(self.ast_is_definitely_valid_up_to, len(self.ast)):
            if not isinstance(self.ast[i], Command):
                return False
        self.ast_is_definitely_valid_up_to = len(self.ast) - 1
        return True

    def deep_repr(self) -> str:
        """A deep and indented string representation of the syntax tree.

        Returns:
            str: The string representation.
        """
        deep_repr_string = ''.join((c.deep_repr() for c in self.ast))
        while '\n\n' in deep_repr_string:
            deep_repr_string = deep_repr_string.replace('\n\n', '\n')
        return deep_repr_string

    def is_running(self) -> bool:
        """Is the interpreter still running.

        Returns:
            bool: The return value.
        """
        return self.runtime.exit_code is None

    def error(self, message: str, trace: str):
        """Cause an error in the syntax tree that might stop execution.
        The type of reaction depends on the `error_mode`.

        Args:
            message (str): The error message to be displayed.
            trace (str): The trace for the error.
        """
        self.throw_error_with_mode(self.error_mode, message, trace)

    def throw_error_with_mode(self, error_mode: ErrorMode,
                              message: str, trace: str):
        """Throw an error with a specified mode.

        Args:
            error_mode (ErrorMode): The error mode to be executed.
            message (str): The error message to be displayed.
            trace (str): The trace for the error.
        """
        if error_mode == ErrorMode.CRASH:
            print(f'\033[31m{message}\n\n{trace}\033[0m')
            self.runtime.exit_code = 1
        elif error_mode == ErrorMode.PRINT:
            print(f'\033[31m{message}\n\n{trace}\033[0m')
        elif error_mode == ErrorMode.SUPPRESS:
            pass
        elif error_mode == ErrorMode.MIRROR_PARENT:
            print(f'\033[31mAN ERROR OCCURRED,\n'
                  f'BUT ERROR MODE "MIRROR PARENT" IS NOT SUPPORTED\n\n'
                  f'{message}\n\n{trace}\033[0m')

    def interpret(self):
        """Interpret the syntax tree to its end.
        """
        while self.execution_index != len(self.ast) and self.is_running():
            command = self.ast[self.execution_index]
            command.execute()
            self.execution_index += 1

    def complete_run(self, run_after_each_line: bool = False) -> int:
        """Build and run the syntax tree.

        Args:
            run_after_each_line (bool, optional): Run after parsing a single
                line. This is used for the shell mode and is not recommended
                when running entire programs. Otherwise it first parses the
                entire tree and then executes it.

        Returns:
            int: The program exit code.
        """
        while 1:
            self.build_token_list(1 if run_after_each_line else None)
            self.guess_variables()
            self.build_token_tree()
            # print(self.deep_repr())
            if self.is_valid():
                self.interpret()
            elif not run_after_each_line:
                print('INVALID SYNTAX\n\n\n', self.deep_repr())

            if not self.is_running():
                return self.runtime.exit_code or 0

            if not run_after_each_line:
                return 0


class SubAst(Ast):
    """An Ast object that is the child of another Ast.
    This is currently used by the braces/group for managing the Ast contained
    within them.

    Attributes:
        parent_ast (Ast): The parent Ast.
    """

    parent_ast: Ast

    def __init__(self, parent_ast: Ast):
        """Initialize the Ast with a parent.

        Args:
            parent_ast (Ast): The parent Ast.
        """
        self.parent_ast = parent_ast
        self.runtime = self.parent_ast.runtime
        super().__init__()

    def error(self, message: str, trace: str):
        if self.error_mode == ErrorMode.MIRROR_PARENT:
            self.parent_ast.error(message, trace)
        else:
            self.throw_error_with_mode(self.error_mode, message, trace)
