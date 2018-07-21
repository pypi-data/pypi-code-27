"""Mara command line interface"""

import logging
import sys

import click

log = logging.getLogger(__name__)


@click.group(help="""\
Runs contributed commandline commands

Contributed functionality (ETL runners, downloader,...) are available as subcommands.

To run the flask webapp, use 'flask run'.

""")
@click.option('--debug', default=False, is_flag=True, help="Show debug output")
def cli(debug: bool):
    # --debug is consumed by the setup_commandline_commands but it's here to let it show up in help
    # and not cause parse errors
    pass


def setup_commandline_commands():
    """Needs to be run before click itself is run so the config which contributes click commands is available"""
    commandline_debug = '--debug' in sys.argv
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s, %(name)s: %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        # makefiles expect all log in stdout
                        stream=sys.stdout)

    if commandline_debug:
        logging.root.setLevel(logging.DEBUG)
        log.debug("Enabled debug output via commandline")

    # Initialize the config system
    from mara_config import init_mara_config_once
    init_mara_config_once()

    # The order basically means that the we only get information about the config system startup
    # when --debug is given on the commandline, but not when mara_config.config.debug() is configured
    # in the config system itself.
    # I think we can live with that...
    from mara_config.config import debug as configured_debug
    if configured_debug():
        logging.root.setLevel(logging.DEBUG)
        log.debug("Enabled debug output via config")

    # overwrite any config system with commandline debug switch
    if commandline_debug and not configured_debug():
        from mara_config.config_system import set_config
        set_config('debug', function=lambda: True)

    from mara_config import get_contributed_functionality
    known_names = []
    for module, command in get_contributed_functionality('MARA_CLICK_COMMANDS'):
        if command and 'callback' in command.__dict__ and command.__dict__['callback']:
            package = command.__dict__['callback'].__module__.rpartition('.')[0]
            # Give a package a chance to put all their commands as subcommands of the main package name.
            # For that to work we have to make sure we do not add multiple commands with the same name
            if isinstance(command, click.Group):
                name = command.name
            else:
                name = package + '.' + command.name
            if name in known_names:
                callback = command.__dict__['callback']
                func_name = f"{callback.__module__}{callback.__name__}"
                raise RuntimeError(f"Attempting to add conflicting click.Commands for name '{name}': {func_name}")
            known_names.append(name)
            command.name = name
            cli.add_command(command)


def main():
    """'mara' console_scripts entry point"""
    setup_commandline_commands()
    args = sys.argv[1:]
    cli.main(args=args, prog_name='mara')


if __name__ == '__main__':
    main()
