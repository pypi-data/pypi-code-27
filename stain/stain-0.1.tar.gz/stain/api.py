# -*- coding:utf-8 -*-

"""
stain.api
---------

Implements core stain functionality

Usage::
    >>> from stain import Stain
    >>> stain = Stain()
    >>> stain.BOLD_RED_ON_BLACK
    '\x1b[1m\x1b[31m\x1b[40m'
    >>> print(stain.GREEN + "OK" + stain.RESET)
    'OK'
    >>> with stain.red():
    >>>     print('ERROR')
    'ERROR'
"""

import sys
from contextlib import contextmanager
from functools import partial

ESCAPE_SEQUENCE = "\033["

ALL_FORMATTING = dict(default='39', black='30', red='31',
                      green='32', yellow='33', blue='34',
                      magenta='35', cyan='36', light_gray='37',
                      dark_gray='90', light_red='91', light_green='92',
                      light_yellow='93', light_blue='94', light_magenta='95',
                      light_cyan='96', white='97', on_default='49',
                      on_black='40', on_red='41', on_green='42',
                      on_yellow='43', on_blue='44', on_magenta='45',
                      on_cyan='46', on_light_gray='47', on_dark_gray='100',
                      on_light_red='101', on_light_green='102', on_light_yellow='103',
                      on_light_blue='104', on_light_magenta='105', on_light_cyan='106',
                      on_white='107', bold='1', dim='2',
                      underline='4', blink='5', reverse='7',
                      hidden='8', reset_all='0', reset_bold='21',
                      reset_dim='22', reset_underline='24', reset_blink='25',
                      reset_reverse='27', reset_hidden='28')

SAFE_FORMATTING = dict(default='39', black='30', red='31',
                       green='32', yellow='33', blue='34',
                       magenta='35', cyan='36', light_gray='37',
                       dark_gray='90', light_red='91', light_green='92',
                       light_yellow='93', light_blue='94', light_magenta='95',
                       light_cyan='96', white='97', on_default='49',
                       bold='1', dim='2', underline='4',
                       blink='5', hidden='8', reset_all='0',
                       reset_bold='21', reset_dim='22', reset_underline='24',
                       reset_blink='25', reset_reverse='27', reset_hidden='28')


class Stain():

    def __init__(self, unsafe=False):
        self.isatty = sys.stdout.isatty()

        if unsafe:
            self._valid_formatting = set([k for k in ALL_FORMATTING])
        else:
            self._valid_formatting = set([k for k in SAFE_FORMATTING])

        if self.isatty:
            self.RESET = "\033[0m"
        else:
            self.RESET = ""

    @contextmanager
    def _line_formatter(self, args, **kwargs):
        '''
        print requested control characters and cleanup afterwards

        :param args: list of formatter strings
        :param kwargs: unused

        :return: side-effects (prints formatting on __enter__ and __exit__)
        :rtype: None
        '''
        try:
            for code in args:
                print("{}{}{}".format(ESCAPE_SEQUENCE, ALL_FORMATTING[code], 'm'), end='')
            yield None
        finally:
            print(self.RESET, end='')

    def _constant_formatter(self, args, **kwargs):
        '''
        String representation of codes needed for formatting

        :param args: list of formatter strings
        :param kwargs: unused
        '''

        fmt = "".join([ESCAPE_SEQUENCE + ALL_FORMATTING[code.lower()] + 'm' for code in args])
        return fmt

    @contextmanager
    def _no_tty(self, attr):
        '''
        noop context manager to stop us from printing garbage characters when not in a terminal
        '''
        try:
            yield None
        finally:
            return None

    def _no_tty_constant(self, attr):
        '''
        noop constant builder to stop us from printing garbage characters when not in a terminal
        '''
        return ""

    def __getattr__(self, attr):
        '''
        try to parse attribute and pass along to the correct formatter

        :param attr: the class attribute called in user code

        '''
        raw_args = attr.split('_')
        parsed_args = []
        modifiers = set(['on', 'light', 'dark', 'reset', 'ON', 'LIGHT', 'DARK', 'RESET'])
        skip_next = False

        for i, item in enumerate(raw_args):

            if skip_next:
                if item in modifiers:
                    continue
                else:
                    skip_next = False
                    continue

            if i == len(raw_args) - 1:
                # if we're the last item, it can't be a modifier
                parsed_args.append(item)
            elif item in modifiers:
                skip_next = True
                # handle double modifiers like on_light_gray
                if raw_args[i + 1] in modifiers:
                    parsed_args.append("{0}_{1}_{2}".format(item, raw_args[i + 1], raw_args[i + 2]))
                else:
                    parsed_args.append("{0}_{1}".format(item, raw_args[i + 1]))
            else:
                parsed_args.append(item)
        if raw_args[0].islower():
            # Bail out if we're being redirected
            if not self.isatty:
                return partial(self._no_tty, attr)
            # Send us to the contextmanager if we get lower_case_attrs
            validation = set(parsed_args).difference(self._valid_formatting)
            if len(validation) != 0:
                with self.red():
                    print("Error: invalid formatting argument {}".format(validation))
                raise AttributeError

            return partial(self._line_formatter, parsed_args)
        elif raw_args[0].isupper():
            # Bail out if we're being redirected
            if not self.isatty:
                return self._no_tty_constant(attr)
            # Send us to the "constant" builder if we get stain.UPPER_CASE_ATTRS
            # I know this isn't really what constant means, but users will access
            # as though they are constants
            return self._constant_formatter(parsed_args)
