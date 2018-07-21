class Command(object):
    """
    Base class for all commands that can be run in the Aperture cli.

    When a command is entered, it's mapped to the equivalent child-class
    of Command. If a match is found, the 'run' method of that class is executed.

    Example: User enters 'aperture hello'. The Hello child-class is found (see hello.py).
    The run method of Hello class is executed.
    """

    def __init__(self, options, *args, **kwargs):
        """Initialize the command instance."""

        # TODO: Figure out what each of these do....
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Corresponding code for a command.

        Raises:
            NotImplementedError: The run command of the command child-class is not implemented.
        """
        raise NotImplementedError("Command does not have a run function.")
