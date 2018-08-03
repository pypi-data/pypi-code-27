# -*- encoding: utf-8

import os
import subprocess
import sys

import click

from .helpers import get_changed_paths, run_formatting
from .superprocess import check_call


@click.group()
def cli():
    """platform-cli is a command-line tool for managing build tasks in
    the Wellcome Digital Platform repos."""


@cli.command()
def format():
    """Run autoformatting commands."""
    run_formatting(run_all=True)


@cli.command()
def autoformat():
    """Run autoformatting in Travis."""
    travis_event_type = os.environ['TRAVIS_EVENT_TYPE']
    assert travis_event_type == 'pull_request'
    branch_name = os.environ['TRAVIS_PULL_REQUEST_BRANCH']

    changed_paths = get_changed_paths('HEAD', 'master')

    run_formatting()

    # If there are any changes, push to GitHub immediately and fail the
    # build.  This will abort the remaining jobs, and trigger a new build
    # with the reformatted code.
    if subprocess.call(['git', 'diff', '--exit-code']):
        print('*** There were changes from formatting, creating a commit')

        # We checkout the branch before we add the commit, so we don't
        # include the merge commit that Travis makes.
        git('fetch', 'ssh-origin')
        git('checkout', branch_name)

        git('add', '--verbose', '--update')
        git('commit', '-m', 'Apply auto-formatting rules')
        git('push', 'ssh-origin', 'HEAD:%s' % branch_name)

        # We exit here to fail the build, so Travis will skip to the next
        # build, which includes the autoformat commit.
        sys.exit(1)
    else:
        print('*** There were no changes from auto-formatting')
        sys.exit(0)
