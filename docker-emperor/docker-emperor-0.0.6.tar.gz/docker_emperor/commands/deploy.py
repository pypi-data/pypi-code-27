import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):

    m = root.project.machine

    m.start()
    if m.driver != m.Drivers.LOCALHOST:

        # ex. docker-machine scp -r -d . virtualbox:/home/docker/project.dev.localhost/

        Command(
            m.path,
            'scp',
            '-r',
            '-d',
            '.', 
            '{}:{}'.format(
                m.name, 
                os.path.join('/home/docker/', root.project.compose.compose_path)
            ),
            is_system=True,
            log=True
        )

    root.run_command('build')    
    root.run_command('start')