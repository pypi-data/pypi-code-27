import argparse

def get_description():
    return "Test subcommand."

def set_args(parser):
    parser.add_argument("-n", "--name")

def execute(args):
    print("Hello, " + args.name)