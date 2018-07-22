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
from buildok.util.console import Console


class Report(object):
    """Report wrapper for automated scripts.

    Arguments:
        runtime      (int): Script runtime in seconds.
        status       (str): Human-readable text status (e.g. OK, Failed, Exit).
        topic        (str): Topic as text string.
        total_steps  (int): Total steps found in choosen topic.
        current_step (int): Last step counted while looping instructions.
        error        (str): Human-readable text error (e.g. Permission denied).
    """

    runtime = 0
    status = "n/a"
    topic = "n/a"
    total_steps = 0
    current_step = 0
    error = "n/a"

    @classmethod
    def set_runtime(cls, runtime):
        """Set runtime value.
        """

        cls.runtime = runtime

    @classmethod
    def set_status(cls, status):
        """Set status value.
        """

        cls.status = status

    @classmethod
    def set_topic(cls, topic):
        """Set topic value.
        """

        cls.topic = topic

    @classmethod
    def set_total_steps(cls, total_steps):
        """Set total steps value.
        """

        cls.total_steps = total_steps

    @classmethod
    def set_error(cls, error):
        """Set error value.
        """

        cls.error = error

    @classmethod
    def inc_step(cls, inc):
        """Increment current step value.
        """

        cls.current_step += inc

    @classmethod
    def output(cls):
        """Dump report of each saved property.
        """

        Log.info("""Topic name: "%s" """ % cls.topic)
        Log.info("Steps ran successful %d out of %d" % (cls.current_step, cls.total_steps))
        Log.info("""Last step error: "%s" """ % cls.error)
        Log.info("Runtime %ss" % cls.runtime)
        Log.info("Build %s" % cls.status.upper())
