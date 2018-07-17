

__all__ = ['run']


def run(root, *args, **kwargs):

    root.project.ask_machine()
    root.project.ask_context()