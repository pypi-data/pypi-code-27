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

from buildok.util.log import Log


def scan_lookup(statements, lookup, length=80):
    """Lookup a statement with example usage.

    Args:
        statements (Statement): Statement instance will all known statements.
        lookup           (str): String to lookup after in all statements.
    """

    Log.debug("Lookup after %s ..." % lookup)
    known_statements = statements.get_actions()
    actions = []

    # Check available statements
    if len(known_statements) == 0:
        return Log.error("Statements are missing")

    # Search in all statemnts
    for stmt in known_statements:
        if lookup.lower() in stmt.parse_description().lower():
            if stmt not in actions:
                actions.append(stmt)
        else:
            for exp in stmt.parse_statements():
                if lookup.lower() in exp.lower():
                    if stmt not in actions:
                        actions.append(stmt)

    # Handle missing action
    if len(actions) == 0:
        return Log.error("Nothing found for '%s'" % lookup)

    # Print lookup
    for action in actions:
        print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
        print(u"\033[90m|\033[0m \033[96m%-{}s\033[0m \033[90m|\033[0m".format(length-2) % action.parse_description())
        print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
        for text in action.parse_statements():
            print(u"\033[90m|   |\033[0m \033[95m%-{}s\033[0m \033[90m|\033[0m".format(length-6) % text.strip())
        print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
        for text in action.parse("sample"):
            print(u"\033[90m|   |\033[0m \033[93m%-{}s\033[0m \033[90m|\033[0m".format(length-6) % text.strip())

    # Done
    print(u"\033[90m|%-{}s|\033[0m".format(length-4) % ("-" * (length)))
    Log.debug("Done...")
