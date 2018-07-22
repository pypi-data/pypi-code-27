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

from buildok.statements.service_enable import EnableService

from buildok.util.log import Log


class DisableService(EnableService):
    r"""Disable service at boot time.

    Args:
        srv (str): Service name to disable.

    Retuns:
        str: Output as string.

    Raises:
        OSError: If an invalid `srv` is provided.

    Accepted statements:
        ^disable service `(?P<srv>.+)`$

    Sample (input):
        - Disable service `urandom`.

    Expected:
        Service 'urandom' => disable
    """

    os_distro_trigger = {
        ("arch", "centos", "coreos", "debian", "fedora", "gentoo", "mageia", "mint", "opensuse", "rhel", "suse", "ubuntu"): ("systemctl disable {service}.service", "systemctl is-disabled {service}.service")
    }

    def run(self, srv=None, *args, **kwargs):
        cmd = DisableService.check_systemd()
        if cmd is None:
            return self.fail("Unsupported OS: %s" % self.env.os_name)
        try:
            toggle_cmd, check_cmd = cmd
            service_cmd = toggle_cmd.format(service=srv)
            Log.debug("Service OS (%s) boot: %s ..." % (self.env.os_name, service_cmd))
            service_output = Popen(cmd_split(service_cmd))
            while service_output.poll() is None:
                sleep(0.5)
            if 0 != service_output.returncode:
                return self.fail(u"Service '%s' => failed to disable" % srv)
            ok, status = DisableService.get_status(cmd_split(check_cmd.format(service=srv)))
            output = u"Service '%s' => %s" % (srv, status)
            if not ok:
                self.success(output)
            else:
                self.fail(output)
        except CalledProcessError as e:
            self.fail(e.output)
        except Exception as e:
            self.fail(str(e))
