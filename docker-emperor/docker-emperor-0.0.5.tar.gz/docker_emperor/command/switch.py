

__all__ = ['run']


def run(root, *args, **kwargs):

    root.run_command('context:set')
    root.run_command('machine:set')