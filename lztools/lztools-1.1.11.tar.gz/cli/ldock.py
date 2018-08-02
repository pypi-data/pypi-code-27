#!/usr/bin/env python3
import os

import click

from lztools.Bash import command_result
from lztools.text import regex

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """A collection of python tools and bash commands for git by Laz aka nea"""
    pass

@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("-a" "--all", is_flag=True, default=True)
def kill():
    """test"""
    pass

@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("-p", "--path", default=".")
def branch(path):
    """Gets the active branch"""
    print(os.getcwd())
    for x in regex(r"\* (.*)", command_result("git", "branch")[1]):
        print(x)

if __name__ == '__main__':
    main()
