import click

from clusterone import authenticate
from clusterone import client
from clusterone.utilities.jobs_table import prepare_jobs_table_rows


@click.command()
@click.pass_obj
@authenticate()
def command(context):
    """
    List notebooks
    """
    _command(context)


def _command(context, api_client=client, prepare_row_func=prepare_jobs_table_rows, print_function=click.echo):
    """Actual command function. Made a separate function to be unit-testable"""

    click.secho("Notebooks are in alpha, unexpected behavior is expected.", fg="yellow")

    notebooks = api_client.get_notebooks()
    if not notebooks:
        print_function("You don't seem to have any notebooks yet. Try just create a notebook to make one.")
        return

    table = prepare_row_func(notebooks)
    print_function(table)
