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

from os import environ

from buildok.util.log import Log


class Placeholder(object):
    """Parse guide and replace palceholders with defined values.

    It works with an environment variable PLACEHOLDERS which stores the absolute
    path to a placeholder-holder file. Data stored inside the file has to follow
    the format:

        key1=value1
        key2=value2_value2.2
        keyX=768g2eyd921h81z

    Shell arguments can overwrite any key defined in placeholder file. Sample
    usage:

        --placeholder key1=newValue1 --placeholder key2=newPlaceholder

    Raises:
        Exception: If specified placeholder file is invalid.
    """

    storage = None

    @classmethod
    def config(cls, args):
        """Configure placeholder class instance.

        Args:
            args (list): Provided by shell; updates internal placeholder storage

        Raises:
            Exception: If file provided by environment variable is not valid
        """

        if not isinstance(cls.storage, dict):
            cls.storage = {}
        ph_file = environ.get("PLACEHOLDERS")
        if ph_file is not None:
            try:
                with open(ph_file) as fd:
                    data = fd.read().split("\n")
                    cls.storage.update(cls.parse_args(data))
            except Exception as e:
                raise SystemExit(str(e))
        cls.storage.update(cls.parse_args(args))

    @classmethod
    def parse_args(cls, args):
        """Arguments parser.

        Arguments must have the following format:

            key1=value1
            key2=value2

        Args:
            args (list): List of arguments to be parsed.

        Returns:
            dict: Dictionary of paired arguments as key-value.
        """

        if not isinstance(args, list):
            args = []
        return dict([tuple(kv.split("=", 1)) for kv in args if len(kv) > 1])

    @classmethod
    def parse_string(cls, string):
        """Key-value string parser.

        Replaces a string containing a placeholder with it's stored value.

        Args:
            string (str): String to scan and update.

        Returns:
            str: Updated string.
        """

        for k, v in cls.storage.iteritems():
            string = string.replace("<%s>" % k, v)
        return string

    @classmethod
    def scan_string(cls, string):
        """Placeholder scanner.

        Scan a string for placeholders.

        Args:
            string (str): String to scan.

        Returns:
            bool: True if string has placeholders.
        """

        for k in cls.storage.iterkeys():
            if "<%s>" % k in string:
                return True
        return False

    @classmethod
    def parse_list(cls, list_string):
        """Key-value list parser.

        Replaces a string containing a placeholder with it's stored value.

        Args:
            list_string (list): List of strings to scan and update.

        Returns:
            list: Updated list of strings.
        """

        return [cls.parse_string(s) for s in list_string]

    @classmethod
    def scan_list(cls, list_string):
        """Placeholder scanner.

        Scan a list of strings for placeholders.

        Args:
            list_string (list): List of strings to scan.

        Returns:
            bool: True if list has placeholders.
        """

        return any([cls.scan_string(s) for s in list_string])
