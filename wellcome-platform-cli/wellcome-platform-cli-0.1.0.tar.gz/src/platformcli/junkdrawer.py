# -*- encoding: utf-8
"""
A miscellaneous collection of functions and helpers for use in the CLI.
Named junkdrawer.py because I haven't prganised it properly.

https://twitter.com/betsythemuffin/status/1003313844108824584

"""

from .superprocess import check_output


def get_changed_paths(*args):
    """
    Returns a set of changed paths in a given commit range.

    :param commit_range: Arguments to pass to ``git diff``.
    """
    diff_output = check_output('git', 'diff', '--name-only', *args)

    return set([
        line.strip()
        for line in diff_output.splitlines()
    ])


def run_formatting(run_all=False):
    """
    Run all the formatting scripts.
    """
    if run_all or any(f.endswith(('.sbt', '.scala')) for f in changed_paths):
        check_call('sbt', 'scalafmt')

    if run_all or any(f.endswith('.tf') for f in changed_paths):
        check_call('terraform', 'fmt')
