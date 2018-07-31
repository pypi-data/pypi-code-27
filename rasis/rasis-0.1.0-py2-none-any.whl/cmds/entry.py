# -*- coding: utf-8 -*-

"""Module entry contains the entrypoint.
"""

import click
import cmds.crawl
import cmds.analyse

@click.group()
def entry():
    pass

entry.add_command(cmds.crawl.crawl)
entry.add_command(cmds.analyse.puc)
