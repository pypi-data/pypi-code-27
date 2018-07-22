# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

from os import environ

from buildok.version import __version__

from buildok.statement import Statement
from buildok.script import Script
from buildok.report import Report
from buildok.action import Action
from buildok.placeholder import Placeholder

from buildok.util.console import Console
from buildok.util.shell import Shell
from buildok.util.analyze import self_analyze, analyze, crash
from buildok.util.locker import lock, unlock
from buildok.util.lookup import scan_lookup
from buildok.util.sysenv import Sysenv
from buildok.util.log import Log


def main(error=None):

    # Parse command line args
    args = Shell.parse()

    # System setup
    Sysenv.setup(__version__, args)

    # Check version and exit
    if args.version:
        return Sysenv.print_version()

    # Output application intro headers
    Sysenv.print_headers()

    # Set log verbose level
    Log.configure(verbose=args.verbose)

    # Set console verbose level
    Console.verbose = args.verbose

    # Prepare all statements
    Statement.prepare()

    # Lookup statement and example usage
    if args.lookup is not None:
        return scan_lookup(Statement, args.lookup)

    # Run analysis and exit
    if args.analyze:
        return analyze(Statement)

    # Self-analyze buildok and continue or crash
    self_analyze(None, Statement) or crash("Run an analyze and correct problems")

    # Setup placeholders
    Placeholder.config(args.placeholder)

    # Attach system environment to all actions
    Action.set_env(Sysenv)

    # Initialize script and run all steps
    guide_script = Script(args)
    guide_script.setup()

    # Create a lock file
    lock()
    try:

        # Parse guide and run all steps
        guide_script.parse().run()

    except Exception as e:
        if str(e) != "":
            error = e

    # Free lock file
    unlock()

    # Display report
    guide_script.print_report()

    # Throw any errors found...
    if environ.get("DEBUG") is not None and error is not None:
        raise Console.fatal(error)
