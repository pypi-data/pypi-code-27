import logging
import os
from _mysql import OperationalError

from tornado.options import options

import middleware
from middleware import config
from middleware.model import MiddlewareModel

config.initialize()


def create_db_structure():
    path = os.path.dirname(middleware.__file__)
    for sqlFile in [open(path + "/db/procedures.sql", "r"),
                    open(path + "/db/db_scheme.sql", "r")]:
        sql = sqlFile.read()
        sqlFile.close()
        # all SQL commands (split on ';')
        sqlCommands = sql.split(';')
        # Execute every command from the input file
        with MiddlewareModel.transaction() as cursor:
            for command in sqlCommands:
                # This will skip and report errors
                # For example, if the tables do not yet exist, this will skip over
                # the DROP TABLE commands
                try:
                    cursor.execute(command)
                except OperationalError, msg:
                    logging.warning("Command skipped: ", msg)