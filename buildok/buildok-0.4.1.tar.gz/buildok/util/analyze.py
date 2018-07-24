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


class UnicodeIcon(object):

    VALID = u"\033[92m\u2713\033[0m"
    INVALID = u"\033[91m\u237B\033[0m"


def crash(message):
    """Crash application with message.

    Raises:
        SystemExit.
    """

    return Log.fatal("Unexpected crash! %s" % message)


def scan_statements(statement):
    """Scans all statements.

    Returns:
        dict: Dictionary of all statements with a counter.
    """

    lines = {}
    if statement is None:
        return lines
    for action in statement.get_actions():
        for line in action.parse_statements():
            if lines.get(line) is None:
                lines.update({line: 0})
            lines[line] += 1
    return lines


def self_analyze(lines=None, statement=None):
    """Self analyze for errors.

    Returns:
        bool: True if all statements are ok, otherwise False.
    """

    if lines is None:
        lines = scan_statements(statement)
    return all([v == 1 for v in lines.itervalues()])


def fmt(fmt, txt):
    """Text formatter helper.
    """

    return fmt % txt


def analyze(statement, length=80):
    """Analyze all statements and print visual results.

    Returns:
        bool: True if all statements are ok, otherwise False.
    """

    lines = scan_statements(statement)
    results = self_analyze(lines)
    Log.debug("Listing all statements...")
    for action in statement.get_actions():
        try:
            text = action.parse_description()
        except Exception:
            text = "no description"
        delimiter = "-" * (length-4)
        c_txt = u"\033[96m %-{}s \033[0m".format(length-6)
        r_txt = u"\033[91m %-{}s \033[0m".format(length-6)
        g_txt = u"\033[92m %-{}s \033[0m".format(length-6)
        print(u"\033[90m|---|%-{}s|\033[0m".format(length-4) % delimiter)
        print(u"\033[90m|   |\033[0m" + fmt(c_txt, text) + "\033[90m|\033[0m")
        print(u"\033[90m|---|%-{}s|\033[0m".format(length-4) % delimiter)
        for line in action.parse_statements():
            if lines[line] > 1:
                status = UnicodeIcon.INVALID
                line_text = fmt(r_txt, line.strip())
            else:
                status = UnicodeIcon.VALID
                line_text = fmt(g_txt, line.strip())
            print_line = u"\033[90m|\033[0m " + status + u" \033[90m|\033[0m"
            print_line += line_text + u"\033[90m|\033[0m"
            print(print_line)
    print(u"\033[90m|---|%-{}s|\033[0m".format(length-4) % delimiter)
    if not results:
        Log.error("Duplicated statements found!")
        for line, times in lines.iteritems():
            if times > 1:
                err = (times, line.strip())
                Log.error(" - line duplicated %d times: %s" % err)
        Log.error("Please correct these problems before running again.")
    else:
        Log.debug("Everything looks OK!")
    return results
