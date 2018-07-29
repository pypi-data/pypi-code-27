#!/usr/bin/env python3
import logging
import os
import sys
from argparse import ArgumentParser

try:
    from colorama import Fore, Style

    DISABLE_COLORS = False
except ImportError:
    DISABLE_COLORS = True

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

VERSION = "1.0.0"


class CommandPathError(Exception):
    pass


class PythonPathUtil:
    """The main class which includes a number of helpers for analyzing and
    diagnosing problems with environment variables that define a list of
    paths."""

    # A successful command returns 0 in UNIX systems
    RETURN_VALUE = 0

    def __init__(self, variable, verbosity=None, no_color=False):
        """Initialize the utility and analyze the environment variable."""
        self.envvar = variable
        self.verbosity = verbosity
        self.no_color = no_color or DISABLE_COLORS
        try:
            self.value = os.environ[self.envvar]
        except KeyError:
            logger.error(
                "Environment variable `{}` not found".format(self.envvar)
            )
            sys.exit(1)
        self.paths = self.value.split(os.pathsep)

    def doctor(self):
        """Identify possible problems with paths in the list."""
        for path in self.paths:
            self._print_path_info(self._get_path_properties(path))

    def can_add(self, new_path, priority=0):
        """Determine if the `new_path` path can be added to the environment
        variable without problems.

        :param str new_path: The path to add to self.envvar
        """
        if new_path in self.paths:
            msg = "Path already in ${} variable".format(self.envvar)
            raise CommandPathError(msg)

        path_properties = self._get_path_properties(new_path)
        full_path = path_properties["full_path"]

        if not path_properties["exists"]:
            raise CommandPathError(
                "Path `{}` does not exist".format(full_path)
            )
        elif not path_properties["is_directory"]:
            raise CommandPathError(
                "Path `{}` is not a directory".format(full_path)
            )
        if not path_properties["is_readable"]:
            raise CommandPathError(
                "Path `{}` is not accessible by the current user".format(
                    full_path
                )
            )

    def _get_path_properties(self, path):
        """Return a set of basic properties as a dictionary for the path
        provided."""
        return {
            "path": path,
            "full_path": os.path.abspath(path),
            "exists": os.access(path, os.F_OK),
            "is_directory": os.path.isdir(path),
            "is_readable": os.access(path, os.R_OK),
        }

    def _print_path_info(self, info):
        """Print information about a path, given a dictionary with its basic
        properties. This will print either a success or an error message."""
        if not info["exists"]:
            msg = "does not exist"
            self._handle_error(msg, info["path"])
        elif not info["is_directory"]:
            msg = "is not a directory"
            self._handle_error(msg, info["path"])
        elif not info["is_readable"]:
            msg = "is not accessible by the current user"
            self._handle_error(msg, info["path"])
        else:
            self._handle_success(info["path"])

    def _handle_error(self, message, path):
        """Handle a problematic path.

        Identifying a problem will cause the command to exit with an error code
        of 1. 1 stands for a general error.
        """
        self.RETURN_VALUE = 1
        self._print_error(message, path)

    def _print_error(self, message, path):
        """Print a standard formated error.

        Adjust the message based on the DISABLE_COLORS flag.
        """
        if self.no_color:
            message = "[ERROR] Path `{}` {}".format(path, message)
        else:
            message = "{red}×{reset} Path {red}{path}{reset} {msg}".format(
                red=Fore.RED, reset=Style.RESET_ALL, path=path, msg=message
            )
        logger.error(message)

    def _handle_success(self, path):
        """Handle a checked path."""
        if self.verbosity > 0:
            self._print_good_path(path)

    def _print_good_path(self, path):
        """Print a standard formated message about a checked path.

        Adjust the message based on the DISABLE_COLORS flag.
        """
        if self.no_color:
            message = "[OK] {}".format(path)
        else:
            message = "{green}✓ {path}{reset}".format(
                green=Fore.GREEN, reset=Style.RESET_ALL, path=path
            )
        logger.info(message)


def main(argv=None):
    description = "Update and diagnose paths in environment variables"
    parser = ArgumentParser(description=description)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument(
        "-v", "--verbosity", action="count", help="Increase output verbosity"
    )
    parser.add_argument(
        "--no-color", action="store_true", dest="disable_colors"
    )
    parser.add_argument(
        "--var",
        dest="variable",
        help="The environment variable to check",
        default="PATH",
    )
    parser.add_argument(
        "--can-add",
        dest="candidate",
        help=(
            "Check if a path can be added to the environment variable without "
            "problems"
        ),
    )

    parser.set_defaults(verbosity=0)
    args = parser.parse_args()

    if args.verbosity > 0:
        logger.setLevel(logging.DEBUG)

    if DISABLE_COLORS:
        logger.debug("Colors disabled. Could not find `colorama` library.")

    util = PythonPathUtil(
        args.variable, verbosity=args.verbosity, no_color=args.disable_colors
    )
    # Currently we have two usage options:
    # 1. Check if a given path can be added
    # 2. Perform a check on a provided environment variable that contains paths
    if args.candidate:
        try:
            util.can_add(args.candidate)
        except CommandPathError as error:
            if util.no_color:
                print(util.no_color)
                logger.error("[ERROR] {}".format(str(error)))
            else:
                message = "{red}[× path-diag]{reset} {msg}".format(
                    red=Fore.RED, reset=Style.RESET_ALL, msg=error
                )
                logger.error(message)
            util.RETURN_VALUE = 1
    else:
        try:
            util.doctor()
        except Exception as e:
            logger.error(str(e))
            util.RETURN_VALUE = 1

    sys.exit(util.RETURN_VALUE)


if __name__ == "__main__":
    main()
