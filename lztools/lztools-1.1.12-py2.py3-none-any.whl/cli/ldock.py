#!/usr/bin/env python3

import click

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

if __name__ == '__main__':
    main()
