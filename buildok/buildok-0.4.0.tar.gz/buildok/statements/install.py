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

from subprocess import Popen
from time import sleep
from shlex import split as cmd_split

from buildok.action import Action

from buildok.util.log import Log


class InstallPackage(Action):
    r"""Install new software package(s).

    Args:
        pkgs (str): Packages to install.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        Exception: If any of `pkgs` are not found in repositories.

    Accepted statements:
        ^install `(?P<pkgs>.+)`$

    Sample (input):
        - Install `vim curl`.

    Expected:
        Installed 2 new packages
    """

    os_packs = {
        ("alpine",):            "apk add {packages}",
        ("debian", "ubuntu"):   "apt-get install -y {packages}",
        # ("centos", "fedora"):   "yum install {packages}",
        # ("fedora",):            "dnf install -y {packages}",
        # ("slackware",):         "slackpkg install {packages}",
        # ("arch",):              "pacman -S {packages}",
        # ("gentoo",):            "emerge {packages}",
    }

    def run(self, pkgs=None, *args, **kwargs):
        packages = pkgs.split()
        if len(packages) == 0:
            return self.fail("No packages to install...")
        try:
            cmd = InstallPackage.check_install()
            if cmd is None:
                return self.fail("Unsupported OS: %s" % self.env.os_name)
            installed_pkgs = self.install_packages(cmd, packages)
            if installed_pkgs > 0:
                self.success("Installed %d new packages" % installed_pkgs)
            else:
                self.fail("Failed to install packages...")
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, pkgs=None, *args, **kwargs):
        if pkgs is None:
            return "echo Nothing to install"
        cmd = InstallPackage.check_install()
        if cmd is not None:
            return cmd.format(packages=pkgs)
        return "echo Unable to install packages: %s" % pkgs

    @classmethod
    def check_install(cls):
        for oses, cmd in cls.os_packs.iteritems():
            if cls.env.os_name in oses:
                return cmd
        return None

    def install_packages(self, cmd, packages):
        installed = 0
        for pkg in packages:
            install_cmd = cmd_split(cmd.format(packages=pkg))
            install_output = Popen(install_cmd)
            while install_output.poll() is None:
                sleep(0.5)
            output = install_output.returncode
            Log.debug("Running (%s) %s ... %r" % (self.env.os_name, install_cmd, output == 0))
            if 0 == output:
                installed += 1
        return installed
