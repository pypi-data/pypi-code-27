import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    logger.cmd('Run <b>%s</b>' % (root.project.compose.compose_path, ))
    root.project.machine.start()
    root.run_command('down', internal=True)
    root.run_command('up', *args, internal=True)