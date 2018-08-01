# -*- coding: utf-8 -*-

"""Console script for meix."""
import sys
import click
from meix import message


@click.command()
@click.argument('name', required=False)
def main(name):
    """Console script for meix."""
    name = name or "pretend person"
    message(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
