import os
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.path,
        'restart',
        *args,
        machine=root.project.machine,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is restarted.' % (root.project.compose.compose_path, ))
