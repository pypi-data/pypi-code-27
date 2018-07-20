import os
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):

    
    root.run_command('machine:start')
    if not root.machine.is_localhost:

        # ex. docker-machine scp -r -d . virtualbox:/home/docker/project.dev.localhost/

        root.bash(
            m.path,
            'scp',
            '-r',
            '-d',
            '.', 
            '{}:{}'.format(
                m.name, 
                os.path.join('/home/docker/', root.compose.name)
            ),
            is_system=True,
            log=True
        )

    root.run_command('build')    
    root.run_command('start')