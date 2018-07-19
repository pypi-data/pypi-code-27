import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    if not root.machine.is_running:
        logger.cmd('Start machine <b>%s</b>' % (root.machine.name, ))
        cmd = root.bash(
            root.machine.bin, 
            'start', 
            root.machine.name, 
            *args,
            sys=True
        )
        if cmd.is_success:
            logger.success('Machine <b>%s</b> started.' % (root.machine.name, ))