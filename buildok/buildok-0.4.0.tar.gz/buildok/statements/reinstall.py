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

from buildok.statements.install import InstallPackage


class ReinstallPackage(InstallPackage):
    r"""Reinstall software package(s).

    Args:
        pkgs (str): Packages to reinstall.

    Retuns:
        str: Human readable descriptor message or error.

    Raises:
        Exception: If any of `pkgs` are not found.

    Accepted statements:
        ^reinstall `(?P<pkgs>.+)`$

    Sample (input):
        - Reinstall `vim curl`.

    Expected:
        Reinstalled 2 packages
    """

    os_packs = {
        ("alpine",):            "apk fix {packages}",
        ("debian", "ubuntu"):   "apt-get install --reinstall {packages}",
    }

    def run(self, pkgs=None, *args, **kwargs):
        packages = pkgs.split()
        if len(packages) == 0:
            return self.fail("No packages to reinstall...")
        try:
            cmd = ReinstallPackage.check_install()
            if cmd is None:
                return self.fail("Unsupported OS: %s" % self.env.os_name)
            reinstalled_pkgs = self.install_packages(cmd, packages)
            if reinstalled_pkgs > 0:
                self.success("Reinstalled %d packages" % reinstalled_pkgs)
            else:
                self.fail("Failed to reinstall packages...")
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def convert_shell(cls, pkgs=None, *args, **kwargs):
        if pkgs is None:
            return "echo Nothing to reinstall"
        cmd = ReinstallPackage.check_install()
        if cmd is not None:
            return cmd.format(packages=pkgs)
        return "echo Unable to reinstall packages: %s" % pkgs
