import os


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'top',
        *args,
        machine=root.project.machine,
        is_system=True
    )