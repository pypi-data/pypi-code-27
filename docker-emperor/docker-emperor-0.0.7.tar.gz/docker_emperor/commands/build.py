import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    logger.cmd('Build <b>%s</b>' % (root.project.compose.name, ))
    root.project.machine.start()
    cmd = root.bash(
        root.project.compose.bin, 
        'build',
        *args, 
        machine=root.project.machine,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> built.' % (root.project.compose.name, ))
