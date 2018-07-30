import sys

from lztools.console import main
import Ansi

def add_stdin_arg(name, parser):
    parser.add_argument(name, nargs="*", default=sys.stdin, type=str)

def parse_stdin_arg(value):
    prep = (lambda x: x[:-1]) if type(value).__name__ == "file" else (lambda x: x)
    return (Ansi.strip_reg(prep(x)) for x in value)