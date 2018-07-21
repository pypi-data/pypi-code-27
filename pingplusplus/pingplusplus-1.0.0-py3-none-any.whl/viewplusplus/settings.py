from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def get_argument_parser():
    parser = ArgumentParser(
        description='View++',
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-H', '--host', type=str, help='http host', default="127.0.0.1")
    parser.add_argument('-p', '--port', type=int, help='http port', default=8050)
    parser.add_argument('-g', '--glob', type=str, help='csv file pattern match', default='**/*.csv')
    args = parser.parse_args()
    return args


def get_settings(args):

    # default values:
    settings = Settings(args)
    return settings

class Settings():
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.glob = args.glob