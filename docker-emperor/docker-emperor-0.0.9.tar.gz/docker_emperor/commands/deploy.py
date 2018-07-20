import os
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):

    machine = root.machine

    
    logger.cmd('Deploy project <b>%s</b>' % (root.compose.name, ))
    root.run_command('machine:start', internal=True)
    if not machine.is_localhost:

        # ex. docker-machine scp -r -d . virtualbox:/home/docker/project.dev.localhost/
        for file in machine['files']:
            
            cmd = root.bash(
                root.machine.bin,
                'scp',
                '-r',
                '-d',
                file, 
                '{}:{}'.format(
                    machine.name, 
                    root.machine['workdir']
                ),
                is_system=True,
            )
            print(cmd.cmd_line)
    else:
        logger.warning(machine.LOCAL_MACHINE_WARNING)
