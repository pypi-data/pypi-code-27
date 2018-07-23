"""Defines a command-line interface for experinet."""

import click

import experinet


@click.group()
def cli():
    """Command-line interface for the experinet package."""
    pass


EXP_DOC = "Run all experiments in the given directory."


@cli.command(help=EXP_DOC + (
    "\n\n Arguments:\n\n DIRECTORY  The directory to search for experiments."))
@click.argument("directory", type=str, nargs=1)
@click.option(
    '-r', '--recursive/--flat', default=False,
    help=(
        "Recurse into sub-directories in experiment discovery."
        "Defaults to flat."))
@click.option('-s', '--silent/--verbose', default=False,
              help="Don't print any messages to screen. Defaults to verbose.")
def bydir(directory, recursive, silent):
    """{}""".format(EXP_DOC)
    experinet.run_experiments_by_dir(
        directory=directory, recursive=recursive, silent=silent)
