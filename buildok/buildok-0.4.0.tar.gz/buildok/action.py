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

from buildok.parser import Parser


class Action(object):
    """Action statement base handler.

    Arguments:
        header (str): Lookup docstring header.
        env (Sysenv): System environment instance.

    Args:
        output  (str): Output status message.
        failed (bool): Handler failture status.
        payload (str): Handler payload input message.

    Raises:
        any: Any exception raised by action handler
    """

    env = None
    doc_header = r"accepted statements"

    def __init__(self, payload=None):
        self.payload = payload
        self.output = ""
        self.failed = None

    @classmethod
    def set_env(cls, env):
        """System environment setter.

        Args:
            env (Sysenv): System environment instance.
        """

        if not callable(env):
            raise TypeError("Expected sysenv instance, got something else")
        cls.env = env

    def get_status(self):
        """Action status getter.

        Returns:
            tuple: Boolean if succeded or failed; and output message.
        """

        return (not self.failed, self.output)

    def get_output(self):
        """Output getter.

        Returns:
            str: Output message.
        """

        return self.output

    def set_output(self, message):
        """Output setter.

        Args:
            message (str): Output message.
        """

        self.output = message

    def get_payload(self):
        """Payload getter.

        Returns:
            str: Payload input message.
        """

        return self.payload

    def set_payload(self, payload):
        """Payload setter.

        Args:
            payload (str): Payload input message.
        """

        self.payload = payload

    def success(self, message=""):
        """Flag action as being successful.

        Args:
            message (str): Optional message to describe output.
        """

        self.failed = False
        self.output = message

    def fail(self, message=""):
        """Flag action as being failed.

        Args:
            message (str): Optional message to describe output.
        """

        self.failed = True
        self.output = message

    def has_failed(self):
        """Status getter.

        Returns:
            bool: True if failed, else False.
        """

        return self.failed

    def run(self, *args, **kwargs):
        """Action handler runnable.

        Runs the context of an action handler.

        Raises:
            NotImplementedError: If not implemented.
        """

        raise NotImplementedError("Class must implement this method")

    def before_run(self, *args, **kwargs):
        """Action handler prehook.

        Runs before an action handler.
        """

        pass

    def after_run(self, *args, **kwargs):
        """Action handler posthook.

        Runs after an action handler.
        """

        pass

    def test(self, *args, **kwargs):
        """Action handler testable.

        Tests the context of an action handler.

        Raises:
            NotImplementedError: If not implemented.
        """

        raise NotImplementedError("Class must implement this method")

    @classmethod
    def parse_description(cls, fallback_msg="No description"):
        """Action handler description.

        Returns:
            str: First line from docstring or fallback message.
        """

        try:
            return cls.__doc__.splitlines()[0]
        except IndexError:
            return fallback_msg

    @classmethod
    def parse_statements(cls):
        """Statements parser.

        Returns:
            list: List of statements extracted from action handler.
        """

        return cls.parse(cls.doc_header)

    @classmethod
    def parse(cls, string):
        """Docstring parser.

        Args:
            string (str): Headline string to lookup after.

        Returns:
            list: List extracted from action handler.
        """

        return Parser.lookahead(unicode(cls.__doc__), string)
