# -*- coding: utf-8 -*-
# __author__ = elkan1788@gmail.com

from ppytools.lang.timerhelper import timemeter

import logging
import pymysql

logger = logging.getLogger(__name__)


def closeCursor(cur):
    try:
        cur
    except Exception as e:
        logger.error('MySQL server connect is not ready!!! Err: {}'.format(str(e)))
    else:
        cur.close()


class MySQLClient(object):

    def __init__(self, host, user, pswd, db, port=3306, charset='UTF8'):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.db = db
        self.charset = charset
        self.conn = None
        pass

    def getConn(self):
        if self.conn is None:
            conn_args = {'host': self.host, 'port': self.port, 'user': self.user, 'password': self.pswd,
                         'database': self.db, 'charset': self.charset, 'cursorclass': pymysql.cursors.DictCursor}
            try:
                self.conn = pymysql.connect(**conn_args)
            except Exception as e:
                raise ConnectionAbortedError('Get MySQL server[{0}] connect'.format(self.host), e)

        return self.conn

    @timemeter()
    def execQuery(self, sql):
        result = []
        try:
            cur = self.getConn().cursor()
            cur.execute(sql)
            for row in cur.fetchall():
                result.append(row)
        except Exception as e:
            raise Exception('Execute MySQL client query failed!!!', e)
        finally:
            closeCursor(cur)
            records = len(result)

        logger.info('MySQL client query completed. Records found: %d', records)

        return result, records
