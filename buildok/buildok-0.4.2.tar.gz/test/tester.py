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

from buildok.action import Action
from buildok.parser import Parser
from buildok.statement import Statement
from buildok.util.sysenv import Sysenv
from buildok.structures.instruction import Instruction


def main():

    # Load statemets
    Statement.prepare()

    # Attach sysenv to actions
    Action.set_env(Sysenv)

    # Holder
    not_testing = []

    # Loop all actions
    for action in Statement.get_actions():

        # Get name and description
        action_name = action.__name__
        action_desc = action.parse_description()

        # Get input and output
        data_in = Parser.lookahead(unicode(action.__doc__), "sample input")
        data_out = Parser.lookahead(unicode(action.__doc__), "expected")

        # Avoid actions with no tests
        if len(data_in) == 0:
            not_testing.append((action_name, action_desc))
            continue

        # Validate action
        print("Testing... %s (%s)" % (action_name, action_desc))

        for line in data_in:
            print(" " * 10, line.strip())

            scan = Instruction.PATTERN.match(line.strip())
            if scan is None:
                continue
            step = Instruction(0, scan.group("step"), scan.group("punct"))

            for exp, handler in Statement.get_statements():
                args = exp.match(step.get_step())
                if args is not None:
                    fun = handler()
                    fun.run(**args.groupdict())
                    print(fun.get_output())
                    break

        for line in data_out:
            print("Results...", line.strip())
        print("\n")

    # Print actions with no tests
    print("-" * 10, "\nNot tested...")
    for each in not_testing:
        print(" - %s (%s)" % each)
