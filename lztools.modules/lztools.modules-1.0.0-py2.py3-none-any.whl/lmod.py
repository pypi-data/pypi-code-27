#!/usr/bin/env python3

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """A collection of python tools and bash commands for manipulating text by laz aka nea"""
    pass

if __name__ == '__main__':
    main()
