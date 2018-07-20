import logging
import os
from subprocess import list2cmdline
import sys

from munch import Munch

from tox.config import parseconfig
from tox.exception import ConfigError

from .collector import Collector

log = logging.getLogger(__name__)


class ToxIni(Collector):

    def _collect(self):

        if not (self.path / "tox.ini").exists():
            return

        try:
            toxconf = parseconfig([])
        except ConfigError as exc:
            self._warn_exc(exc)
            return

        name = "py%d%d" % (sys.version_info.major, sys.version_info.minor)
        for key in sorted(toxconf.envconfigs.keys()):
            if key.startswith(name):
                config = toxconf.envconfigs[key]
                break
        else:
            log.warning("%r has no %s environment", self, name)
            return

        # dependencies
        for dep in config.deps:
            if dep.name.startswith("-r"):
                reqs_file = dep.name[2:].strip()
                if not (self.path / reqs_file).exists():
                    log.warning(
                        "%r %r from tox.ini does not exist",
                        self,
                        reqs_file,
                    )
                    continue
                self.add_requirements_file(reqs_file, "test")
            else:
                self.add_requirement(str(dep), "test")

        # environment
        env = Munch()
        for key in config.setenv.keys():
            if key in ("PYTHONHASHSEED", "PYTHONPATH"):
                continue
            env[key] = config.setenv[key].replace(os.getcwd(), ".")

        # commands
        commands = []
        for command in config.commands:
            if command[0] == "pip":
                log.warning("%r ignoring command %r", self, command)
            else:
                cmd = []
                for expr in command:
                    cmd.append(expr.replace(os.getcwd(), "."))
                cmd = list2cmdline(cmd).strip()
                if cmd.startswith("-"):
                    cmd = "%s || true" % cmd[1:].strip()
                commands.append(cmd)

        self.ext.tox = Munch(commands=commands, env=env)
