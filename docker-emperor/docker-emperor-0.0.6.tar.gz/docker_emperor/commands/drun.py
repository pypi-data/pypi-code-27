import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    logger.cmd('Run <b>%s</b> as deamon' % (root.project.compose.compose_path, ))
    root.project.machine.start()
    root.run_command('down')
    root.run_command('up -d', *args)