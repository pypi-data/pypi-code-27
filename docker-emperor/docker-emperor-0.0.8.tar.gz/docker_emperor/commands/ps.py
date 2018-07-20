import os


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'ps',
        *args,
        machine=root.project.machine,
        is_system=True
    )