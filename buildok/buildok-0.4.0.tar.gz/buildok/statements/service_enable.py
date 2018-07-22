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


class EnableService(Action):
    r"""Enable service at boot time.

    Args:
        srv (str): Service name to enable.

    Retuns:
        str: Output as string.

    Raises:
        OSError: If an invalid `srv` is provided.

    Accepted statements:
        ^enable service `(?P<srv>.+)`$

    Sample (input):
        - Enable service `urandom`.

    Expected:
        Service 'urandom' => enabled
    """

    os_distro_trigger = {
        ("arch", "centos", "coreos", "debian", "fedora", "gentoo", "mageia", "mint", "opensuse", "rhel", "suse", "ubuntu"): ("systemctl enable {service}.service", "systemctl is-enabled {service}.service")
    }

    def run(self, srv=None, *args, **kwargs):
        cmd = EnableService.check_systemd()
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
                return self.fail(u"Service '%s' => failed to enable" % srv)
            ok, status = EnableService.get_status(cmd_split(check_cmd.format(service=srv)))
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
            if line.lower().strip().startswith("enabled"):
                return True, "enabled"
        return False, "disabled"

    @classmethod
    def check_systemd(cls):
        for oses, cmds in cls.os_distro_trigger.iteritems():
            if cls.env.os_name in oses:
                return cmds
        return None

    @classmethod
    def convert_shell(cls, srv=None, *args, **kwargs):
        if srv is None:
            return "echo Invalid script or missing service"
        cmd, _ = cls.check_systemd()
        if cmd is not None:
            return cmd.format(service=srv)
        return "echo Unable to get status of service %s" % srv
