from docker_emperor.command import Command


def run(root, *args, **kwargs):

    root.project.machine.start()
    Command(
        root.project.compose.path, 
        'build',
        *args, 
        machine=root.project.machine,
        sys=True
    )