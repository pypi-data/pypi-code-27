import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    if not root.machine.is_running:
        if root.machine.is_startable:
            logger.cmd('Start machine <b>%s</b>' % (root.machine.name, ))
            cmd = root.bash(
                root.machine.bin, 
                'start', 
                root.machine.name, 
                *args,
                sys=True
            )
            if root.machine.is_running:
                root.logger.success('Machine <b>%s</b> started.' % (root.machine.name, ))
        else:
            root.logger.warning('Machine <b>%s</b> is not startable.' % (root.machine.name, ))

    return root.machine.is_running

# class Command():

#     def run(self, *args, **kwargs):
#         if not self.interna
#         self.success('Machine <b>%s</b> started.' % (root.machine.name, ))