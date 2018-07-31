# -*- coding: utf-8 -*-

"""Module analyse contains commands about some basic analysis of the data.
"""

import click
import ranker.ranker

@click.command()
@click.option('--workdir', '-w', type=str, default='data',
    help='Specify the work directory. Default: ./data')
@click.option('--tune-info', '-t', nargs=2, type=str, default=('For UltraPlayers', 'hvn'),
    help='Title and diff of the tune. Example: -t "For UltraPlayers" hvn')
def puc(workdir, tune_info):

    analyzer = ranker.ranker.Ranker(workdir)

    click.echo('PUC Players of %s[%s]' % (tune_info[0], tune_info[1]))
    try:
        click.echo(analyzer.puc(tune_info).to_string())
    except IndexError:
        click.echo('Tune Not Found.')
