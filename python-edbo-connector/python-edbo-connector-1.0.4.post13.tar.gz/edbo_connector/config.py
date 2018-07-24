#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import getenv

EDBO_SERVER = getenv('EDBO_SERVER', '')
EDBO_USER = getenv('EDBO_USER', '')
EDBO_PASSWORD = getenv('EDBO_PASSWORD', '')
EDBO_APPLICATION_KEY = getenv('EDBO_APPLICATION_KEY', '')

ECHO_ON = bool(getenv('ECHO_ON', True))
EXECUTION_TIMEOUT = int(getenv('EXECUTION_TIMEOUT', 0))
CONNECTION_RETRIES = int(getenv('CONNECTION_RETRIES', 30))
RELOGIN_AFTER = int(getenv('RELOGIN_AFTER', 60 * 15))
USER_AGENT = getenv('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
MAX_REQUESTS_COUNT = int(getenv('MAX_REQUESTS_COUNT', 15000))
