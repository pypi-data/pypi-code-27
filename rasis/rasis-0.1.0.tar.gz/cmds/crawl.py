# -*- coding: utf-8 -*-

"""Module crawl contains the command crawl.

Usage:
    $ rasis crawl

Command crawl crawls score data from the sdvx official site with scrapy.
You need to provide KONAMI ID and password to login.

Score Ranking Page:
    https://p.eagate.573.jp/game/sdvx/iv/p/ranking/index.html

"""

import click
import crawler.crawler
import getpass
import os

@click.command()
@click.option('--workdir', '-w', type=str, default='data',
    help='Specify the output directory.')
@click.option('--splash-url', '-s', type=str, default='http://127.0.0.1:8050',
    help='Specify the spalsh url.')
def crawl(workdir, splash_url):

    if not os.path.exists(workdir):
        os.makedirs(workdir)
    else:
        if os.path.exists(workdir + '/crawler.log'):
            os.remove(workdir + '/crawler.log')

    username = raw_input('Your Username(KONAMI ID):')
    password = getpass.getpass('Password:')

    crawler.crawler.start(username, password,
        splash_url=splash_url, work_dir=workdir)
