from functools import partial
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.shortcuts import create_eventloop
from threading import Event
from .application import get_application
from .settings import get_settings, get_argument_parser
from .ping_worker import ping_worker
from .ping import pingHasPermission

def run():
    args = get_argument_parser()

    if 'help' in args:
        return

    if not pingHasPermission():
      return

    eventloop = create_eventloop()
    interrupt = Event()
    settings = get_settings(args)

    application = get_application()

    cli = CommandLineInterface(application=application, eventloop=eventloop)
    cli.settings = settings
    cli.interrupt_ping_worker = interrupt
    cli.messagebox = ''

    try:
        ping_worker_callback = partial(ping_worker, cli, interrupt)
        eventloop.run_in_executor(ping_worker_callback)
        cli.run()

    finally:
        eventloop.close()
        interrupt.set()


if __name__ == '__main__':
    run()
