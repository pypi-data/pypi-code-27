import logging
import os
from pathlib import Path
import sys
from subprocess import list2cmdline

from munch import munchify

from tox.config import parseconfig
from tox.exception import ConfigError

from ..requirement import Requirement
from .collector import Collector

log = logging.getLogger(__name__)


class ToxIni(Collector):

    def _collect(self):

        if not Path("tox.ini").exists():
            return

        try:
            toxconf = parseconfig([])
        except ConfigError:
            return

        commands = []
        setenv = dict()

        name = "py%d%d" % (sys.version_info.major, sys.version_info.minor)
        config = toxconf.envconfigs.get(name)
        if config is None:
            return

        for command in config.commands:
            if command[0:2] == ["pip", "install"]:
                req = Requirement.from_line(list2cmdline(command[2:]))
                self.add_requirement(req)
            else:
                cmd = []
                for expr in command:
                    cmd.append(expr.replace(os.getcwd(), "."))
                cmd = list2cmdline(cmd).strip()
                if cmd.startswith("-"):
                    cmd = "%s || true" % cmd[1:].strip()
                commands.append(cmd)
        for req in config.deps:
            if req.name.startswith("-r"):
                reqs_file = req.name[2:]
                if not Path(reqs_file).exists():
                    log.warning(
                        "%r %r from tox.ini does not exist",
                        self,
                        reqs_file,
                    )
                    continue
                self.add_requirements_file(reqs_file)
            else:
                self.add_requirement(req)
        for key in config.setenv.keys():
            if key in ("PYTHONHASHSEED", "PYTHONPATH"):
                continue
            setenv[key] = config.setenv[key].replace(os.getcwd(), ".")
        self.dist.ext.tox = munchify(dict(
            commands=commands,
            setenv=setenv,
        ))
