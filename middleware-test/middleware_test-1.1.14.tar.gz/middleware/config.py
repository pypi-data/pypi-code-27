# -*- coding: utf-8 -*-
import errno
import json
import logging as log
# python imports
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'lib'))

# External imports
from tornado.options import (
    define, options, parse_command_line, parse_config_file
)


def initialize(app_env={}, args=None):
    parse_command_line(args)
    set_env(environments)
    if app_env:
        set_env(app_env)
    parse_command_line(args)
    config_file = os.path.join(os.getcwd(), 'config', '%s.conf') % get_env()
    create_config_file(config_file)
    parse_config_file(config_file)

def create_config_file(file_path):
    if not os.path.exists(file_path):
        import middleware
        path = os.path.dirname(middleware.__file__)
        config = open(path + "/config/example.conf", "r")
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_path, "w") as f:
            f.write(config.read())
        f.close()

def get_env():
    if options.env:
        return options.env
    elif os.getenv('MIDDLEWARE_ENV'):
        options.env = os.getenv('MIDDLEWARE_ENV')
        return os.getenv('MIDDLEWARE_ENV')
    else:
        log.warning("Couldn't determine environment, exiting. Please 'export MIDDLEWARE_ENV=local' or specify "
                    "'--env=local'")


def set_env(environments):
    env_options = environments.get(get_env(), {})
    for setting, value in env_options.items():
        if hasattr(options, setting):
            setattr(options, setting, value)


# Environment
define('env', default='local', help='[Required or set MIDDLEWARE_ENV] Environment (local, dev, staging, prod)',
       type=str)
define('config', default=None, help='Set path to system configuration file', type=str)
define('debug_mode', default=True)
define('autoreload', default=False)
define('port', 8080)

define('root_url', default='localhost')

# Mysql Credentials etc
# GRANT create, alter, references, index, select, insert, update, delete, drop, lock tables ON `octopus-colend`.* TO
# 'dba_dude' IDENTIFIED BY '0pwudZ9uXmQw';
# GRANT select, insert, update, delete, lock tables ON `octopus-colend`.* TO 'octopus' IDENTIFIED BY 'yC86ROIslHtC';
define('mysql_user', default='root')
define('mysql_password', default='')
define('mysql_2_password', default='')
define('schema_user', default='root')
define('schema_password', default='')

# Mysql setup etc
define('middleware_db_ip', default='127.0.0.1')
define('middleware_db_instance', default="middleware")
define('middleware_db_name', default="octopus-middleware")

define('AD_server', default="")
define('AD_admin', default="")
define('AD_password', default="")
define('AD_base_dn', default='')

define('slack_api_url', default="https://slack.com/api/")
define('slack_api_token', default="")

define('logs_expires', default=7)

define('selectHR_db_name', default='')
define('selectHR_db_host', default='')
define('selectHR_db_user', default='')
define('selectHR_db_password', default='')
define('selectHR_driver', default='ODBC Driver 13 for SQL Server')
define('selectHR_audit_db_name', default='')

define('slack_api_tokens_dict', default={})
define('save_picture_path', default='')
define('officevibe_url', default='https://app.officevibe.com/api/v2')
define('officevibe_key', default='')
define('log_slack_requests', default=False)
define('csv_path',
       default='')
define('report_user_email',
       default=None)
define('report_date',
       default=None)
define('report_system',
       default=None)

DEV = 'dev'
PROD = 'prod'

environments = {
    'local': {'logging': 'debug',
              'autoreload': True,
              },

    'dev': {
        'logging': 'debug',
        'debug_mode': True,
    },

    'prod': {
        'logging': 'debug',
        'debug_mode': False,
    },
}


PER_PAGE = 50  # default number of rows in a paginated query
PAGE_SIZES = [10, 20, 50, 100, 200]

