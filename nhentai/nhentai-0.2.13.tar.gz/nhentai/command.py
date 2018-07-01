#!/usr/bin/env python2.7
# coding: utf-8
from __future__ import unicode_literals, print_function
import signal
import platform

from nhentai.cmdline import cmd_parser, banner
from nhentai.parser import doujinshi_parser, search_parser, print_doujinshi, login_parser
from nhentai.doujinshi import Doujinshi
from nhentai.downloader import Downloader
from nhentai.logger import logger
from nhentai.constant import BASE_URL
from nhentai.utils import generate_html, generate_cbz


def main():
    banner()
    logger.info('Using mirror: {0}'.format(BASE_URL))
    options = cmd_parser()

    doujinshi_ids = []
    doujinshi_list = []

    if options.login:
        username, password = options.login.split(':', 1)
        logger.info('Login to nhentai use credential \'%s:%s\'' % (username, '*' * len(password)))
        for doujinshi_info in login_parser(username=username, password=password):
            doujinshi_list.append(Doujinshi(**doujinshi_info))

    if options.keyword:
        doujinshis = search_parser(options.keyword, options.page)
        print_doujinshi(doujinshis)
        if options.is_download:
            doujinshi_ids = map(lambda d: d['id'], doujinshis)
    else:
        doujinshi_ids = options.id

    if doujinshi_ids:
        for id_ in doujinshi_ids:
            doujinshi_info = doujinshi_parser(id_)
            doujinshi_list.append(Doujinshi(**doujinshi_info))

    if not options.is_show:
        downloader = Downloader(path=options.output_dir,
                                thread=options.threads, timeout=options.timeout)

        for doujinshi in doujinshi_list:
            doujinshi.downloader = downloader
            doujinshi.download()
            if not options.is_nohtml and not options.is_cbz:
                generate_html(options.output_dir, doujinshi)
            elif options.is_cbz:
                generate_cbz(options.output_dir, doujinshi)

        if not platform.system() == 'Windows':
            logger.log(15, '🍻 All done.')
        else:
            logger.log(15, 'All done.')

    else:
        [doujinshi.show() for doujinshi in doujinshi_list]


def signal_handler(signal, frame):
    logger.error('Ctrl-C signal received. Quit.')
    exit(1)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
