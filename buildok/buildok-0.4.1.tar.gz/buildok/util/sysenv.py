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

from os import listdir
from platform import system

from buildok import __build__


DISCLAIMER = r"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class Sysenv(object):
    """System environment wrapper.

    Used in various files as a bash ENV-like to determine OS-related calls.

    app_version  (str): Application version (v0.0.0).
    os_name      (str): Operating System name.
    os_version   (str): Operating System version.
    shell_args (Shell): Shell instance with arguments.
    """

    app_version = ""
    os_name = ""
    os_version = ""
    shell_args = None

    @classmethod
    def print_disclaimer(cls):
        """Outputs application disclaimer.
        """

        print(DISCLAIMER)

    @classmethod
    def print_support(cls):
        """Outputs support message.
        """

        print("Please report bugs at https://github.com/lexndru/buildok")
        print("Use --help to see a list of all options")

    @classmethod
    def print_version(cls):
        """Outputs application version.
        """

        v_app, v_os = cls.app_version, cls.os_version
        print("Buildok {} [build {}] {}".format(v_app, __build__, v_os))

    @classmethod
    def print_headers(cls):
        """Output application version, disclaimer and support.
        """

        # Print version
        cls.print_version()
        print("")

        # Print disclaimer
        cls.print_disclaimer()
        print("")

        # Print support
        cls.print_support()
        print("")

    @classmethod
    def setup(cls, version, args):
        """Setup system environment.
        """

        cls.shell_args = args

        # Exit if version is missing
        if not version:
            raise SystemExit("Invalid launch")

        # Set app version
        cls.app_version = version

        # Buildok version header
        cls.os_version = ""

        # Basic support for windows systems
        if system().lower() == "windows":
            cls.os_version = u"WINDOWS"
            cls.os_name = "win"

        # Extended support for macos systems
        elif system().lower() == "darwin":
            cls.os_version = u"MACINTOSH"
            cls.os_name = "mac"

        # Full support for linux systems
        elif system().lower() == "linux":
            files = [f for f in listdir("/etc") if f.endswith("-release")]
            distro, pretty_name = "", ""
            for each_file in files:
                data = []
                with open("/etc/%s" % each_file, "r") as fd:
                    data = fd.readlines()
                for line in data:
                    line_ = line.lower()
                    if line_.startswith("id") and distro == "":
                        _, distro = line.split("=", 1)
                    if line_.startswith("pretty_name") and pretty_name == "":
                        _, pretty_name = line.split("=", 1)
            os_name = distro.strip()
            clean_name = pretty_name.strip()
            cls.os_version = u"%s (%s)" % (os_name.upper(), clean_name)
            cls.os_name = os_name

        # Extended or full support for bsd systems
        elif "bsd" in system().lower():
            cls.os_version = "BSD"
            cls.os_name = "bsd"
