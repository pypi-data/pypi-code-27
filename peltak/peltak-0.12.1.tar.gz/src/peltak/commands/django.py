# -*- coding: utf-8 -*-
"""
Django related management commands.

Those commands replace the usage of ``./manage.py`` (thus it's removed). Those
correspond 1 to 1 to their ``./manage.py`` counterparts but the arguments are
in the fabric format (can't get around this).
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys
from os import environ

# 3rd party imports
import click

# local imports
from peltak.core import conf
from . import cli


@cli.group()
def django():
    """ Commands related to django """
    pass


def _manage_cmd(cmd, settings=None):
    """ Run django ./manage.py command manually.

    This function eliminates the need for having ``manage.py`` (reduces file
    clutter).
    """
    sys.path.insert(0, conf.get('SRC_DIR'))

    settings = settings or conf.get('DJANGO_SETTINGS', None)
    environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    args = sys.argv[0:-1] + cmd

    execute_from_command_line(args)


@django.command()
@click.option('-p', '--port', type=int, default=8000)
@click.option('-s', '--settings', type=str)
def devserver(port=8000, settings=None):
    """ Run dev server. """
    _manage_cmd(['runserver', '0.0.0.0:{}'.format(port)], settings)


@django.command()
def collectstatic():
    """ Collect all static files. """
    _manage_cmd(['collectstatic', '--no-input'])


@django.command()
@click.argument('app')
@click.argument('name')
def mkmigrations(app, name):
    """ Create migrations for a given app. """
    _manage_cmd(['makemigrations', '-n', name] + app.split(' '))


@django.command()
def migrate():
    """ Apply pending migrations. """
    _manage_cmd(['migrate'])


@django.command()
def createsuperuser():
    """ Create super user (probably needed for the first user). """
    _manage_cmd(['createsuperuser'])


@django.command()
def shell():
    """ Start django shell """
    _manage_cmd(['shell'])
