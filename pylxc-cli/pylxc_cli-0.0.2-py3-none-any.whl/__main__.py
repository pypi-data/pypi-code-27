#!/usr/bin/env python
"""This module uses the lxc library."""
from pylxc.liblxc import liblxc
import click


@click.group()
def cli():
    pass


cli.add_command(liblxc.lxc.list)
cli.add_command(liblxc.lxc.rename)
cli.add_command(liblxc.lxc.stop)
cli.add_command(liblxc.lxc.start)
cli.add_command(liblxc.lxc.create)
cli.add_command(liblxc.lxc.remove)

if __name__ == '__main__':
    cli()
