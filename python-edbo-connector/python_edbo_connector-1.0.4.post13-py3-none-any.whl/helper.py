#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
EDBOWebApiHelper
Author: Eldar Aliiev
Email: e.aliiev@vnmu.edu.ua
"""

from __future__ import print_function
import os
import sys
import platform
import datetime
from .config import ECHO_ON


class EDBOWebApiHelper:
    """EDBOWebApiHelper - class which implements helper methods"""

    @staticmethod
    def echo(message: str, color: str = None, force_exit: bool = False, clear: bool = False):
        """Print information message to default output
        :param message: Information message
        :param color: Color of output (Default=None)
        :param force_exit: Color of output (Default=False)
        :param clear: Clear screen before output (Default=False)W
        :type message: str
        :type color: str
        :type force_exit: bool
        :type clear: bool
        """
        if ECHO_ON:
            # Clear output
            if clear is True:
                EDBOWebApiHelper.clear_output()

            # Colored output
            if color is not None:
                # Get color char code
                color_code = {
                    'red': '0;31',
                    'green': '0;32',
                    'yellow': '1;33',
                    'cyan': '0;36',
                    'blue': '0;34',
                    'white': '1;37'
                }.get(color, '0')
                print('\033[%sm[%s] %s\033[0m' % (color_code, str(datetime.datetime.now()), message))
            else:
                # Simple output
                print('[%s] %s' % (str(datetime.datetime.now()), message))

            # Need force exit from program
            if force_exit:
                sys.exit()

    @staticmethod
    def format_file_size(size_of_file: int, suffix: str = 'B') -> str:
        """Humanize file size.
        :param size_of_file: Size of file in bytes
        :param suffix: Suffix which will be added to size format
        :type size_of_file: int
        :type suffix: str
        :return: Humanized file size
        :rtype: str
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(size_of_file) < 1024.0:
                return "{0}{1:s}{2:s}".format(
                    round(size_of_file, 3),
                    unit,
                    suffix
                )
            size_of_file /= 1024.0

    @staticmethod
    def clear_output():
        """Clear user output"""
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux':
            os.system('clear')

    @staticmethod
    def save_image(image_content: bytes, save_to: str):
        """Save image bytes ti file"""
        with open(save_to, 'wb') as image_file:
            image_file.write(image_content)
