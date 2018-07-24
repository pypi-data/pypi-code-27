import atuin
from atuin.commands import subcommand, argument
from atuin.core import CORE_LOGGER as log
from atuin.core.initialize import init_atuin_directory, check_atuin_init
from atuin.core.management import get_template, create_challenge_tree
from atuin.core.management import sanitize_challenge_name, challenge_add_template


@subcommand()
def status(arg):
    """print status of current version"""
    # TODO: Actually do something useful here
    print(atuin.__version__)


@subcommand([argument('name', type=str, nargs='+', help='Challenge Name'),
             argument('-p', '--points', type=int, help='Challenge Point Value'),
             argument('-t', '--template', type=str, default='default', help='Custom Template File')],
            'Create a challenge or other object')
def create(arg):
    """Creates a challenge with given templates"""
    if not check_atuin_init():
        log.warning('Current directory is not initialized')
        exit(1)

    template = get_template(arg.template)

    for name in arg.name:
        filename = sanitize_challenge_name(name)
        path = create_challenge_tree(filename)

        if path is None:
            exit(1)

        challenge_add_template(name, filename, path, template, arg.points)


@subcommand([argument('-f', '--force', action='store_true', help='Force reinitialize'),
             argument('dir', type=str, nargs='?', help='Directory to initialize'),
             argument('--config', type=str, help='File or URI for configuration options')],
            'Initialize Atuin')
def init(arg):
    """Initializes the current or given directory for atuin"""
    if not init_atuin_directory(arg.dir, arg.config, arg.force):
        exit(1)
    else:
        exit(0)
