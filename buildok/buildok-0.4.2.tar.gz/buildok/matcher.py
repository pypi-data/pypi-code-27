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

from buildok.statement import Statement


class Matcher(object):
    """A small wrapper to pair statements and steps.

    Requires statements to be processed before running matching algorithm.
    """

    @classmethod
    def is_valid(cls, text_step):
        """Check if step is supported by statements.

        Args:
            text_step (str): Text string of step to check.

        Returns:
            bool: True if statements have support for step.
        """

        step = text_step.strip()
        if len(step) == 0:
            return False
        for exp, _ in Statement.get_statements():
            if exp.match(step) is not None:
                return True
        return False

    @classmethod
    def pair_all(cls, instructions):
        """Loop through all instructions and pair each step.

        Args:
            instructions (list): List of instructions.

        Returns:
            bool: True if all steps have been paired successfully.
        """

        return all([cls.pair_one(i) for i in instructions])

    @classmethod
    def pair_one(cls, instruction):
        """Pair instruction with statement.

        Args:
            instruction (Instruction): An instruction instance to pair.

        Returns:
            bool: True if instruction has a pair whitin statements.
        """

        for exp, fun in Statement.get_statements():
            args = exp.match(instruction.get_step())
            if args is not None:
                instruction.set_description(fun.parse_description())
                instruction.set_statement(fun)
                instruction.set_arguments(args.groups())
                instruction.set_kwarguments(args.groupdict())
                return True
        return False
