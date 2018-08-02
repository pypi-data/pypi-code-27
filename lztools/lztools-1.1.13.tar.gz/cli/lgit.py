import os

import click

from lztools.Bash import command_result
from lztools.text import regex

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """lztools for git"""

@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("-b", "--bash-format", is_flag=True, default=False)
def branch(bash_format):
    """Gets the active branch"""
    if not bash_format:
        for x in regex(r"\* (.*)", command_result("git", "branch")):
            print(x)
    else:
        git_branch = regex(r"\* (.*)", command_result("git", "branch"), only_first=True, suppress=True)
        if git_branch is not None:
            print(f"({git_branch}) ")