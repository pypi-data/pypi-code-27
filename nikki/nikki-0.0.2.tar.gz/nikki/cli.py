import click
from . import nikki as nikki
import splogger as log
import os.path as iou

require_status      = nikki.require_status
STATUS_DECRYPTED    = nikki.STATUS_DECRYPTED
STATUS_INITIALIZED  = nikki.STATUS_INITIALIZED
STATUS_NONE         = nikki.STATUS_NONE

"""
NIKKI   The secured diary

nikki add       add a folder in journal path
nikki delete    delete a folder in journal path
nikki git       call a git command
nikki init      init a new journal
nikki show      show a journal entry (with markdown support)
nikki search    search a word in the journal
nikki edit      open the editor for this joural entry
nikki           drop in cli
"""

@click.group()
def cli():
    pass

@cli.command()
def init():
    require_status(STATUS_NONE)

    nikki.init_journal()
    nikki.encrypt_journal()


LENIENT_CONTEXT = dict(ignore_unknown_options=True, allow_extra_args=True)
@cli.command('git', context_settings=LENIENT_CONTEXT)
@click.pass_context
def git(args):
    require_status(STATUS_INITIALIZED)
    nikki.git_call(args.args)

@cli.command()
@click.argument('path', nargs=-1)
def delete(path):
    require_status(STATUS_INITIALIZED)

    nikki.remove_entry(path)

@cli.command()
@click.argument('path', nargs=-1)
def add(path):
    require_status(STATUS_INITIALIZED)
    nikki.add_entry(path)

@cli.command()
def show():
    require_status(STATUS_INITIALIZED)
    nikki.print_journal()

@cli.command()
@click.argument('args', nargs=-1)
def search(args):
    require_status(STATUS_DECRYPTED)
    log.error('Not implemented: search')

@cli.command()
@click.argument('path', nargs=-1)
def edit(path):
    require_status(STATUS_DECRYPTED)
    nikki.edit(path)
    nikki.encrypt_journal()

