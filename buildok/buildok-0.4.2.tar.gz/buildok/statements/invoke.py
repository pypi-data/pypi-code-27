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

from buildok.action import Action


class InvokeTopic(Action):
    r"""Invoke another topic from guide.

    Args:
        topic (str): Topic complete name to invoke.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        Exception: If an invalid `topic` is provided.

    Accepted statements:
        ^read (?:steps from )?topic `(?P<topic>.+)`$
        ^continue reading topic `(?P<topic>.+)`$
        ^follow steps from `(?P<topic>.+)`$

    Sample input:
        - Follow steps from `do something else`.

    Expected:
        Running new topic => do something else
    """

    def run(self, topic=None, *args, **kwargs):
        pass
