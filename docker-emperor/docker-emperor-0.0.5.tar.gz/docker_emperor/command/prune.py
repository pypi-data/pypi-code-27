import os
from docker_emperor.command import Command
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):
    
    for sys in ['system', 'network', 'volume']:
        Command(
            root.docker_path,
            sys,
            'prune',
            machine=root.project.machine,
            sys=True
        )