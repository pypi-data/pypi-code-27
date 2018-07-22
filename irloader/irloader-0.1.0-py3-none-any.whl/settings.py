from argparse import ArgumentParser #, ArgumentDefaultsHelpFormatter
import pathlib

def get_argument_parser():
    parser = ArgumentParser(description='ir loader') #formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--ir-file',     required=True,  type=pathlib.Path, help='ir file path')
    parser.add_argument('-l', '--looper-file', required=False, type=str, help='source file for looper', default='')
    args = parser.parse_args()
    return args

def get_settings(args):

    # default values:
    settings = Settings(args)
    return settings

class Settings():
    def __init__(self, args):

        if not args.ir_file.is_file():
            raise SystemExit("{} does not exists".format(args.ir_file))
        self.ir_file = str(args.ir_file)

        if args.looper_file and not pathlib.Path(args.looper_file).is_file():
            raise SystemExit("{} does not exists".format(args.looper_file))

        self.looper_file = str(args.looper_file)
        self.looper = self.looper_file != ""
        
