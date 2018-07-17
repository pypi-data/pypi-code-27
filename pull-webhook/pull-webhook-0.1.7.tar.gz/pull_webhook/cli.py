# -*- coding: utf-8 -*-
"""Console script for pull_webhook."""
import sys
import click
from pull_webhook import Puller
from pull_webhook import main as launch_server


@click.command()
@click.option('--remote', default='origin')
@click.option('--branch', default='master')
@click.option('--port', default=8888)
@click.argument('repository_directory')
def main(remote, branch, port, repository_directory):
    Puller.remote = remote
    Puller.branch = branch
    Puller.repository_directory = repository_directory
    launch_server(port=port)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
