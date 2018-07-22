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

from re import compile, IGNORECASE, UNICODE


class Instruction(object):
    """Blueprint of an instruction.

    Class arguments:
        PATTERN  (RegEx): Regular expression of an instruction.
        RunType (object): Class object of steps punctuation.

    Args:
        order       (int): Runtime order as found in topic.
        step        (str): Instruction step as text.
        punct       (str): Punctuation step as text.
        payload     (str): Instruction payload as input.
        action (callable): Action handler from installed statements.
        args      (tuple): Action arguments after applying expression to step.
        kwargs     (dict): Action keyword arguments after applying expression to step.
        status     (bool): Instruction status after action handler run.
        output      (str): Instruction output after action handler run.

    Raises:
        TypeError: If invalid datatype is provided.
    """

    PATTERN = compile(
        r"^(?:\-|\d+\))\s+(?P<step>.+)(?<=[^\.\:\;])(?P<punct>[\.\:\;]{1})$",
        IGNORECASE|UNICODE
    )

    class RunType(object):
        """Statement action punctuation.

        Used to determine action type for a statement.

        Possible values:
          . = Run statement.
          ; = Run statement and continue only if succeeds.
          : = Run statement with content as input params.
        """

        END = "."
        AND = ";"
        ARGS = ":" # has payload

    def __init__(self, order=None, step=None, punct=None):
        self.order = order
        self.step = step
        self.punct = punct
        self.action = None
        self.args, self.kwargs = None, None
        self.payload = None
        self.description = None
        self.status = None
        self.output = None

    def get_status(self):
        """Instruction status getter.

        Returns:
            bool: Instruction run status.
        """

        return self.status

    def get_output(self):
        """Instruction output getter.

        Returns:
            str: Instruction run output.
        """

        return self.output

    def set_payload(self, payload):
        """Instruction payload setter.

        Has support for sequences-based datatypes.

        Args:
            payload (mixt): Instruction payload.

        Raises:
            TypeError: If unsupported data is provided.
        """

        if isinstance(payload, (tuple, list, set, frozenset)):
            self.payload = "\n".join(payload)
        elif isinstance(payload, (str, unicode)):
            self.payload = payload
        else:
            raise TypeError("Unsupported payload provided")

    def get_payload(self):
        """Instruction payload getter.

        Returns:
            str: Instruction payload.
        """

        return self.payload

    def set_position(self, value):
        """Instruction position setter.

        Args:
            value (int): Instruction position order.

        Raises:
            TypeError: If value is not an unsigned interger.
        """

        if not isinstance(value, int) or value < 0:
            raise TypeError("Position must be an unsigned integer")
        self.order = value

    def get_position(self):
        """Instruction position getter.

        Returns:
            int: Instruction order.
        """

        return self.order

    def set_step(self, value):
        """Instruction step setter.

        Args:
            value (str): Instruction raw step as text.

        Raises:
            TypeError: If value is not a non-empty string.
        """

        if not isinstance(value, (str, unicode)) or len(value) == 0:
            raise TypeError("Step must be non-empty string")
        self.step = value

    def get_step(self):
        """Instruction text step getter.

        Returns:
            str: Instruction text step string.
        """

        return self.step

    def set_description(self, value):
        """Instruction description setter.

        Args:
            value (str): Instruction description as text.

        Raises:
            TypeError: If value is not a non-empty string.
        """

        if not isinstance(value, (str, unicode)) or len(value) == 0:
            raise TypeError("Description must be non-empty string")
        self.description = value

    def get_description(self):
        """Instruction description getter.

        Returns:
            str: Instruction description string.
        """

        return self.description

    def set_statement(self, value):
        """Instruction action statement setter.

        Args:
            value (callable): Instruction step handler.

        Raises:
            TypeError: If value is not callable.
        """

        if not callable(value):
            raise TypeError("Step handler must be callable")
        self.action = value

    def get_statement(self):
        """Instruction action statement getter.

        Returns:
            callable: Instruction step handler.
        """

        return self.action

    def set_arguments(self, value):
        """Instruction action arguments setter.

        Args:
            value (tuple): Instruction step arguments.

        Raises:
            TypeError: If value is not tuple.
        """

        if not isinstance(value, tuple):
            raise TypeError("Step arguments must be tuple")
        self.args = value

    def get_arguments(self):
        """Instruction action arguments getter.

        Returns:
            tuple: Instruction step arguments.
        """

        return self.args

    def set_kwarguments(self, value):
        """Instruction action keyword arguments setter.

        Args:
            value (dict): Instruction step keyword arguments.

        Raises:
            TypeError: If value is not dict.
        """

        if not isinstance(value, dict):
            raise TypeError("Step arguments must be dict")
        self.kwargs = value

    def get_kwarguments(self):
        """Instruction action keyword arguments getter.

        Returns:
            dict: Instruction step keyword arguments.
        """

        return self.kwargs

    def set_punctuation(self, value):
        """Instruction punctuation setter.

        Args:
            value (str): Instruction punctuation string.

        Raises:
            TypeError: If value is not a valid punctuation.
        """

        if value not in self.RunType.__dict__.values():
            raise TypeError("Unsupported step punctuation")
        self.punct = value

    def get_punctuation(self):
        """Instruction punctuation getter.

        Returns:
            Punctuation: Instruction punctuation flag.
        """

        return self.punct

    def run(self):
        """Run instruction.

        Raises:
            TypeError: If action is not callable or is not set.

        Returns:
            tuple: (Boolean) True if succeeds, otherwise False; (String) output.
        """

        if not callable(self.action):
            raise TypeError("Action is not set")
        handler = self.action()
        handler.before_run()
        handler.set_payload(self.payload)
        if not isinstance(self.kwargs, dict):
            self.kwargs = {}
        if not isinstance(self.args, tuple):
            self.args = ()
        if len(self.kwargs) >= len(self.args):
            handler.run(**self.kwargs)
        else:
            handler.run(*self.args)
        handler.after_run()
        self.status, self.output = handler.get_status()
        return self.status, self.output

    def __repr__(self):
        return unicode(self.__dict__)
