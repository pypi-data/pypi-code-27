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

from shlex import split as cmd_split
from subprocess import Popen, CalledProcessError, PIPE

from buildok.action import Action

from buildok.util.log import Log


class StatusService(Action):
    r"""Get status of service.

    Args:
        srv (str): Service name to retrieve status.

    Retuns:
        str: Output as string.

    Raises:
        OSError: If an invalid `srv` is provided.

    Accepted statements:
        ^get status (?:for|of) service `(?P<srv>.+)`$
        ^Print `(?P<srv>.+)` service status$

    Sample (input):
        - Get status of service `urandom`.

    Expected:
        Service 'urandom' => active
    """

    os_distro = {
        ("arch", "centos", "coreos", "debian", "fedora", "gentoo", "mageia", "mint", "opensuse", "rhel", "suse", "ubuntu"): "systemctl status {service}.service"
    }

    def run(self, srv=None, *args, **kwargs):
        cmd = StatusService.check_systemd()
        if cmd is None:
            return self.fail("Unsupported OS: %s" % self.env.os_name)
        try:
            service_cmd = cmd.format(service=srv)
            Log.debug("Service OS (%s) status: %s ..." % (self.env.os_name, service_cmd))
            ok, status = StatusService.get_status(cmd_split(service_cmd))
            output = u"Service '%s' => %s" % (srv, status)
            if ok:
                self.success(output)
            else:
                self.fail(output)
        except CalledProcessError as e:
            self.fail(e.output)
        except Exception as e:
            self.fail(str(e))

    @classmethod
    def get_status(cls, service_cmd):
        proc = Popen(service_cmd, stdout=PIPE)
        stdout, _ = proc.communicate()
        for line in stdout.split("\n"):
            # https://www.freedesktop.org/software/systemd/man/systemctl.html
            if not line.lower().strip().startswith("active: "):
                continue
            if "active (running)" in line.lower():
                return True, "active"
            elif "deactivating" in line.lower():
                return False, "deactivating"
            elif "activating" in line.lower():
                return True, "activating"
            elif "failed" in line.lower():
                return False, "failed"
            elif "inactive" in line.lower():
                return False, "inactive"
        return False, "n/a"

    @classmethod
    def check_systemd(cls):
        for oses, cmd in cls.os_distro.iteritems():
            if cls.env.os_name in oses:
                return cmd
        return None

    @classmethod
    def convert_shell(cls, srv=None, *args, **kwargs):
        if srv is None:
            return "echo Invalid script or missing service"
        cmd = cls.check_systemd()
        if cmd is not None:
            return cmd.format(service=srv)
        return "echo Unable to get status of service %s" % srv
