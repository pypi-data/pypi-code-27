from __future__ import absolute_import, division, print_function, unicode_literals

import os
from typing import Union
from os.path import join, dirname
from dotenv import load_dotenv
import unittest
import vcr
from unittest import TestCase
from logging import getLogger

logger = getLogger(__name__)
vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)
dotenv_path: Union[bytes, str] = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


class PackageTest(TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
