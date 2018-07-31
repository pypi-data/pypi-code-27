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
nikki encrypt   encrypt files not detected as encrypted with the given password
nikki           drop in cli
"""

@click.group()
def cli():
    pass

@cli.command()
def init():
    """
    Init or reset the journal
    """
    require_status(STATUS_NONE)

    nikki.init_journal()
    nikki.encrypt_journal()


LENIENT_CONTEXT = dict(ignore_unknown_options=True, allow_extra_args=True)
@cli.command('git', context_settings=LENIENT_CONTEXT)
@click.pass_context
def git(args):
    """
    Use git
    """
    require_status(STATUS_INITIALIZED)
    nikki.git_call(args.args)

@cli.command()
@click.argument('path', nargs=-1)
def delete(path):
    """
    Delete an entry (folder)
    """
    require_status(STATUS_INITIALIZED)

    nikki.remove_entry(path)

@cli.command()
@click.argument('path', nargs=-1)
def add(path):
    """
    Add an entry (folder)
    """
    require_status(STATUS_INITIALIZED)
    nikki.add_entry(path)

@cli.command()
def show():
    """
    Print the journal's arborescence
    """ 
    require_status(STATUS_INITIALIZED)
    nikki.print_journal()

@cli.command()
@click.argument('args', nargs=-1)
def search(args):
    """
    Search in the journal
    """
    require_status(STATUS_DECRYPTED)
    log.error('Not implemented: search')

@cli.command()
@click.argument('path', nargs=-1)
def edit(path):
    """
    Edit a file in the journal
    """
    require_status(STATUS_DECRYPTED, git_commit_message='Edited '+''.join(path))
    nikki.edit(path)

@cli.command()
def encrypt():
    """
    Decrypt and re encrypt everything
    """
    require_status(STATUS_DECRYPTED, git_commit_message='Forced journal encryption')


    #nikki.encrypt_journal(check_encryption=True)

