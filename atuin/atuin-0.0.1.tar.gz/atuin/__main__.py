from atuin.commands import parser
from atuin.commands import *


def main():
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    main()
