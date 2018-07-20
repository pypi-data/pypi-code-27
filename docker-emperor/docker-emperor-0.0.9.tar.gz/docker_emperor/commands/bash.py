import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):
    root.bash(
        *args,
        # machine=root.project.machine,
        is_system=True
    )