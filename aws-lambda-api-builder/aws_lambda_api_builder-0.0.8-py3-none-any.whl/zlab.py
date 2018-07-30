import argparse
import importlib
import pkgutil

from api_builder import configuration, subcommands


def get_module_parser(mod, modname, parents=[], add_help=True):
    """
    Returns an argument parser for the sub-command's CLI.

     :param mod: the sub-command's python module
     :param modnam: the string name of the python module
     :return: ArgumentParser
    """
    return argparse.ArgumentParser(
        usage=configuration.EXECUTABLE_NAME + ' ' + modname + ' [options]',
        description=mod.get_description(), parents=parents,
        add_help=add_help)


def get_application_parser(commands):
    """
    Builds an argument parser for the application's CLI.

    :param commands:
    :return: ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description=configuration.APPLICATION_DESCRIPTION,
        usage =configuration.EXECUTABLE_NAME + ' [sub-command] [options]',
        add_help=False)

    parser.add_argument(
        'sub_command',
        choices=[name for name in commands],
        nargs="?")

    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    return parser


def get_module(name):
    """
    Convenience method for importing a module (i.e. sub-command) from a string

    :param name: module name to import
    :return: the module object
    """
    return importlib.import_module("api_builder.subcommands." + name)

def print_version():
    print("Version: " + configuration.VERSION)

def main():

    sub_commands = [m.name for m in pkgutil.iter_modules(subcommands.__path__)]
    application_parser = get_application_parser(sub_commands)
    args = application_parser.parse_known_args()[0]

    # Print help message
    if not args.sub_command:
        if args.help:
            application_parser.print_help()
            print("")
            print_version()
        if args.version:
            print_version()

    # Delegate to sub-command help message
    if args.sub_command and args.help:
        command = get_module(args.sub_command)
        module_parser = get_module_parser(command, args.sub_command)
        command.set_args(module_parser)
        module_parser.print_help()

    # Execute the sub-command
    if args.sub_command and not args.help:
        command = get_module(args.sub_command)
        module_parser = get_module_parser(command, args.sub_command, parents=[application_parser], add_help=False)
        command.set_args(module_parser)
        module_args = module_parser.parse_args()
        command.execute(module_args)
