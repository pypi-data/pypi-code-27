#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Default Settings

"""


HTTP_PORT = 8888

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

DATABASE = 'sqlite:///db.sqlite3'
