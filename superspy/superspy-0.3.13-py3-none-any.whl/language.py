"""Specify languages and register new commands, functions and other tokens.

When creating a new Language object (usually one should be enough) it will
set the Language.current attribute to itself. New commands and other tokens
or attributes will be added to that language.

Attributes:
    PATTERN (TYPE): The description of the type an argument (=pattern).
    VERBOSE (bool): Load plugins verbosely.
"""

from os import path
import re
from typing import Any, Callable, Dict, List, Optional, Type, Union

from pluginbase import PluginBase

import superspy
from superspy import ast


VERBOSE = True

PATTERN = Union[
    Type['Token'], List[Type['Token']]
]


def bounce(bounce_function: Callable) -> Callable:
    """Inner function required for some decorators. Takes a function
    and returns it.

    Args:
        bounce_function (Callable): The function to be returned.

    Returns:
        Callable: The function that has been passed to the function.
    """
    return bounce_function


##############
# DECORATORS #
##############


def register_data_type(regex: str) -> Any:
    """Registers a new data type matching a specified regex.

    Args:
        regex (str): The regular expression describing the data type.
    """

    def decorator_register(
            data_type_obj: Type['ast.DataType']) -> Type['ast.DataType']:
        """Inner function.

        Args:
            data_type_obj (Type['ast.DataType']): The class to be instantiated
                when matching the regex.

        Returns:
            Type['ast.DataType']: Required for the decorator.
        """
        Language.current.regex_matchers[regex] = data_type_obj
        return data_type_obj

    return decorator_register


def register_token_regex(regex: str) -> Any:
    """Registers a new token matching a specified regex.

    Args:
        regex (str): The regular expression describing the token.
    """

    def decorator_register(token_obj: Type['ast.Token']) -> Type['ast.Token']:
        """Inner function.

        Args:
            token_obj (Type['ast.Token']): The class to be instantiated
                when matching the regex.

        Returns:
            Type['ast.Token']: Required for the decorator.
        """
        Language.current.regex_matchers[regex] = token_obj
        return token_obj

    return decorator_register


def register_token(name: str) -> Any:
    """Register a new token matching a specified name.

    Args:
        name (str): The name matching the token.
    """
    # Escape the Regex, so for example `*` still works and does not match any
    # token. However newlines may not be escaped.
    escaped_re = name
    if name not in ['\n']:
        escaped_re = re.escape(name)

    return register_token_regex(f'^{escaped_re}$')


def register_word_delimiter(character: chr) -> Any:
    """Registers a new word delimiting character.

    Args:
        character (chr): The character that delimits words.
    """

    Language.current.word_delimiters.append(character)
    return bounce


# pylint: disable=invalid-name
# This name is required
def register_single_character_touching_token(character: chr) -> Any:
    """Register a single character token that may touch other characters.

    So for example in `6*7` the `*` is a separate token, even though it is
    touching other characters. Because writing `6 * 7` every time is
    too inconvenient in this world.

    Args:
        character (chr): The character that describes the token.
    """

    def decorator_register(token_obj: Type['ast.Token']) -> Type['ast.Token']:
        """Inner function.

        Args:
            token_obj (Type['ast.Token']): The class to be instantied
                when matching the character.

        Returns:
            Type['ast.Token']: Required for the decorator.
        """
        return register_token(character)(token_obj)

    Language.current.single_character_tokens.append(character)
    return decorator_register


def register_command_with_pattern(*pattern: List[PATTERN]) -> Any:
    """Register a command matching a pattern of arguments and tokens.

    Args:
        *pattern (List[PATTERN]): The pattern to be matched.
    """

    def decorator_register(
            command_obj: Type['ast.Command']) -> Type['ast.Command']:
        """Inner function.

        Args:
            command_obj (Type['ast.Command']): The class to be instantied
                when matching the pattern.

        Returns:
            Type['ast.Command']: Required for the decorator.
        """
        Language.current.all_commands.append(command_obj)

        priority = command_obj.priority
        if priority in Language.current.commands_by_priority:
            Language.current.commands_by_priority[priority].append(command_obj)
        else:
            Language.current.commands_by_priority[priority] = [command_obj]
        command_obj.pattern = pattern

        return command_obj

    return decorator_register


def register_command(command: Type['ast.Command']) -> Any:
    """Register a command matching the pattern described in the `__init__`.

    Args:
        command (Type['ast.Command']): The class to be instantiated
            when matching the character.
    """
    pattern = list(command.__init__.__annotations__.values())
    return register_command_with_pattern(*pattern)(command)


def register_literality_delimiter(opening: str, closing: str) -> Any:
    """Register a pair of strings delimiting literality, like "".

    So everything inside the delimiters is taken literal, even though it
    might contain things like spaces or even commands.

    Args:
        opening (str): The string beginning the literality.
        closing (str): The string closing   the literality.
    """

    Language.current.literality_delimiter[opening] = closing
    return bounce


def register_operator(operator: str) -> Any:
    """Register an operator like `*` or `==` or `equals`.

    Args:
        operator (str): The operator to be registered.
    """

    # pylint: disable=pointless-statement
    @register_single_character_touching_token(operator)
    class OperatorToken(ast.Token):
        """A dumb token representing the operator.
        """
        ...

    def decorator_register(
            function_obj: Type['ast.Function']) -> Type['ast.Function']:
        """Inner function.

        Args:
            function_obj (Type['ast.Function']): The class to be instantiated
                when matching the operator pattern.

        Returns:
            Type['ast.Function']: Required for the decorator.
        """
        pattern = list([ast.Command, OperatorToken, ast.Command])
        register_command_with_pattern(*pattern)(function_obj)
        return function_obj

    return decorator_register


def register_function(function_name: str, argument_count: int = 1) -> Any:
    """Register a function with a specified amount of arguments.

    Args:
        function_name (str): The name of the function.
        argument_count (int, optional): The count of arguments
    """

    # pylint: disable=pointless-statement
    @register_token(function_name)
    class FunctionNameToken(ast.Token):
        """A dumb token representing the function call.
        """
        ...

    def decorator_register(
            function_obj: Type['ast.Function']) -> Type['ast.Function']:
        """Inner function.

        Args:
            function_obj (Type['ast.Function']): The class ot be instantiated
                when matching the function.

        Returns:
            Type['ast.Function']: Required for the decorator.
        """
        pattern = list([FunctionNameToken, *([ast.Command] * argument_count)])
        register_command_with_pattern(*pattern)(function_obj)
        return function_obj

    return decorator_register


def register_falsy_value(falsy_value: str) -> Any:
    """Register a value that is falsy (or not True).

    So for example `while []` will not get executed.

    Args:
        falsy_value (str): The value that is falsy
    """

    Language.current.falsy_values.append(falsy_value)
    return bounce


###########
# CLASSES #
###########


class Language:
    """An object representing a language including commands and syntax.

    It is responsible for independently loading plugins from specified
    searchpaths, registering new commands, tokens etc. and storing this data
    including other attributes like literality delimiters or escape markers
    to be used by the abstract syntax tree for parsing.

    Attributes:
        excluded_plugins (List[str]): List of plugins to not be loaded in the
            specified searchpaths. So if you don't want `io` to be loaded, add
            it here.

        all_commands (List[Type['ast.Command']]): List of all registered
            commands.
        commands_by_priority (Dict[float, List[Type['ast.Command']]]): A
            dictionary that has the priorities (or order of operations) of all
            commands as keys and the command classes as values.

        escape_markers (str): Characters marking to next character to be
            escaped. So for example `\"` does not end the string.
        word_delimiters (List[str]): Characters delimiting words, like spaces.
        regex_matchers (Dict[str, Type['ast.Token']]): The regex to match
            tokens and the token to be instantiated.
        single_character_tokens (List[chr]): Tokens that are only one character
            long, like `*` or `=`.
        literality_delimiter (Dict[str, str]): Literality delimiting pair of
            strings, like `""`.
        falsy_values (List[str]): List of values that evaluate as false like
            `[]`, `""` or `0`.

        plugin_base (TYPE): PluginBase base object
        plugin_source (TYPE): PluginBase source object

        current (Language): Class variable for the currently loading language.
    """

    excluded_plugins: List[str] = []

    all_commands: List[Type['ast.Command']] = []
    commands_by_priority: Dict[float, List[Type['ast.Command']]] = {}
    escape_markers = '\\'
    word_delimiters: List[chr] = []
    regex_matchers: Dict[str, Type['ast.Token']] = {}
    single_character_tokens: List[chr] = []
    literality_delimiter: Dict[str, str] = {}
    falsy_values: List[str] = []

    plugin_base: Any
    plugin_source: Any

    # classvar
    current: 'Language'

    def __init__(self, search_paths: List[str]):
        """Initiate the Language and load Plugins.

        Args:
            search_paths (List[str]): The search path for the plugins.
        """
        Language.current = self
        self.plugin_base = PluginBase(package=f'superspy.system')
        self.plugin_source = self.plugin_base.make_plugin_source(
            searchpath=search_paths)
        for plugin in self.plugin_source.list_plugins():
            if plugin not in self.excluded_plugins:
                if VERBOSE:
                    print(f'\033[36mLoaded plugin\033[0m {plugin}')
                self.plugin_source.load_plugin(plugin)

    def evaluates_as_true(self, statement: str) -> bool:
        """Return this statement evaluated as True.

        Args:
            statement (str): The statement to be evaluated

        Returns:
            bool: The return statements, True if the statement evaluates as
                True, False otherwise.
        """
        return statement not in self.falsy_values


class SuperSpyLanguage(Language):
    """A language subclass automatically loading the superspy plugins.
    """

    superspy_search_paths = ['system']
    default_search_paths = [
        path.join(path.dirname(superspy.__file__), superspy_search_path)
        for superspy_search_path in superspy_search_paths]

    def __init__(self,
                 custom_search_paths: Optional[List[str]] = None,
                 excluded_plugins: Optional[List[str]] = None):
        """Summary

        Args:
            custom_search_paths (Optional[List[str]], optional): Adding custom
                searchpaths, for plugins used for this shell.
            excluded_plugins (Optional[List[str]], optional): Ignore specific
                plugins. These can be in the custom search path, or in the
                default library. So for example ['io', 'arithmetic'] would not
                load those two plugins.
        """
        search_paths = self.default_search_paths + (custom_search_paths or [])
        self.excluded_plugins = (excluded_plugins or [])
        super().__init__(search_paths)
