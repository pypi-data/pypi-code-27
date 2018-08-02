# -*- coding: utf-8 -*-

import functools
import logging
# python imports
import os
import re
import time
import traceback
from contextlib import contextmanager
from datetime import datetime

import MySQLdb
# external imports
from tornado.options import options

# project imports



class MysqlModel(object):

    DATABASE_INSTANCE = ''
    DATABASE_GENERATION = ''
    DATABASE_NAME = ''
    HOSTNAME = 'localhost'
    CHARSET = 'utf8'
    TABLE = 'NONE'
    query_type = 'db_query'

    @classmethod
    @contextmanager
    def transaction(cls):
        db = cls.initdb()
        cursor = db.cursor()
        yield cursor
        db.commit()
        cursor.close()

    @classmethod
    def initdb(cls):
        retry = 0
        while retry < 2:
            try:
                params = {
                    'host': cls.HOSTNAME,
                    'port': 3306,
                    'db': cls.DATABASE_NAME,
                    'user': options.mysql_user,
                    'passwd': options.mysql_password,
                    'charset': cls.CHARSET
                }
                return MySQLdb.connect(**params)
            except MySQLdb.OperationalError as oe:
                retry += 1
                traceback.print_exc()
                logging.warning('Retry #%d' % retry)
                time.sleep(1)

                raise

    @classmethod
    def pk(cls):
        return '{}_id'.format(cls.TABLE)

    @classmethod
    def find(cls, order_by=None, **kwargs):
        """ Find all instances of the given class based
            on an exact match of attributes.

            For example:
            User.find(first_name='Bob', last_name='Smith')

            Will return all matches.

            Args:
                order_by (str): String defining order of the results.
                kwargs: Columns and values to filter by.

            Returns:
                List of dicts with results.
        """
        cls.query_type = 'db_query'
        query = "SELECT * FROM {}".format(cls.TABLE)
        params = None
        if kwargs:
            params = cls.dict_to_where(kwargs)
            query += " WHERE {}".format(params.pop(0))
        if order_by:
            query += " ORDER BY {}".format(order_by)
        return cls.process_query(query, params)

    @classmethod
    def count(cls, **attrs):
        """
            User.count(first_name='Bob')

            Return number of items
        """
        cls.query_type = 'db_query'
        if attrs:
            param = cls.dict_to_where(attrs)
            query = "SELECT COUNT(*) FROM %s WHERE %s AND delete_dttm IS NULL" \
                % (cls.TABLE, param[0])
            instances = cls.process_query(query, param[1:],)
        else:
            query = "SELECT COUNT(*) FROM %s WHERE delete_dttm IS NULL" % cls.TABLE
            instances = cls.process_query(query)
        return instances[0]['COUNT(*)']

    @classmethod
    def _insert_one(cls, cursor, **kwargs):
        if 'create_dttm' not in kwargs:
            kwargs['create_dttm'] = datetime.now()
        keys = kwargs.keys()
        sql = """INSERT INTO {} ({}) VALUES ({})""".format(
            cls.TABLE, ','.join(kwargs.keys()), ','.join(['%s'] * len(keys))
        )
        logging.debug("SQL query: %s %s" % (sql, kwargs))
        cursor.execute(sql, kwargs.values())
        return cursor.lastrowid

    @classmethod
    def insert(cls, **kwargs):
        cls.query_type = 'db_insert'
        with cls.transaction() as cursor:
            return cls._insert_one(cursor, **kwargs)

    @classmethod
    def insert_many(cls, items):
        cls.query_type = 'db_insert'
        with cls.transaction() as cursor:
            return [cls._insert_one(cursor, **item) for item in items]

    @classmethod
    def insert_or_update(cls, **kwargs):
        cls.query_type = 'db_insert'
        update = datetime.now()
        kwargs['create_dttm'] = datetime.now()
        keys = kwargs.keys()
        l = len(keys)
        sql = "INSERT INTO {} ({}) VALUES ({})".format(
            cls.TABLE, ','.join(keys), ','.join(['%s'] * l)
        )
        sql += " on duplicate key update update_dttm=%s, delete_dttm=null "
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s %s" % (sql, kwargs))
            # check
            cursor.execute(sql, kwargs.values() + [update])
            return cursor.lastrowid

    @classmethod
    def update(cls, where, **kwargs):
        cls.query_type = 'db_update'
        # if the first argument is not a dict, treat it as ID
        if not isinstance(where, dict):
            where = {cls.pk(): where}
        kwargs_keys, kwargs_values = zip(*kwargs.items())
        values = map('{}=%s'.format, kwargs_keys)
        where = cls.dict_to_where(where)
        sql = "UPDATE {} SET {}, {} WHERE {}".format(
            cls.TABLE,
            ', '.join(values),
            cls.pk() + '=' + cls.pk(),
            where.pop(0)
        )
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s %s %s" % (sql, kwargs_values, where))
            cursor.execute(sql, list(kwargs_values) + where)
            return cursor.lastrowid

    @classmethod
    def db_update(cls, where, **kwargs):
        cls.query_type = 'db_update'
        # if the first argument is not a dict, treat it as ID
        if not isinstance(where, dict):
            where = {cls.pk(): where}
        kwargs_keys, kwargs_values = zip(*kwargs.items())
        values = map('{}=%s'.format, kwargs_keys)
        where = cls.dict_to_where(where)
        sql = "UPDATE {} SET {} WHERE {}".format(
            cls.TABLE,
            ', '.join(values),
            where.pop(0)
        )
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s %s %s" % (sql, kwargs_values, where))
            cursor.execute(sql, list(kwargs_values) + where)
            return cursor.lastrowid

    @staticmethod
    def date_handler(obj):
        """
        Return the object passed in isoformat if possible otherwise log a warning and return obj
        Args:
            obj:

        Returns:

        """
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            logging.warning(obj.dir)
            return obj

    @classmethod
    def paginated(cls, page, per_page=None, total_count=0):
        """ Wrapper that patches the class to allow for paginated queries.

            Args:
                page (int): Number of the page being selected (starts with 1).
                per_page (int): Number of items per page; if omitted, config.PER_PAGE is used.

            Returns:
                Subclass of the wrapped class with ``process_query`` replaced with a partial.
        """
        cls.query_type = 'db_query'
        paginated_cls = type('Paginated{}'.format(cls.__name__), (cls,), {'total_count': 0})
        paginated_cls.process_query = functools.partial(paginated_cls.process_query, page=page, per_page=per_page)
        return paginated_cls

    @classmethod
    def process_query(cls, query, params=(), get_result=True, page=None, per_page=None):
        """ Executes the query with given params, optionally paginated.

            Args:
                query (str): SQL query to be executed.
                params (iter): Iterator providing values to replace "%s" placeholders in the query.
                get_result (bool): If false, just the lastrowid is returned.
                page (int): Number of the page being selected (starts with 1).
                per_page (int): Number of items per page; if omitted, config.PER_PAGE is used.

            Returns:
                List of results as dicts, or an integer if ``get_result`` is False.
        """
        query = query.strip().rstrip(';')
        is_paginated = page is not None and query.lower().startswith('select')
        if per_page is None:
            per_page = config.PER_PAGE
        if is_paginated:
            query = re.sub(r'(select) (.*)', r'\1 SQL_CALC_FOUND_ROWS \2', query, flags=re.I)
            query += ' LIMIT %s OFFSET %s'
            params = list(params) + [per_page, max((page - 1, 0)) * per_page]
        with cls.transaction() as cursor:
            logging.debug("SQL query: {} {}".format(query, params if params else ""))
            cursor.execute(query, params)
            results = cursor.fetchall()
            lastrowid = cursor.lastrowid
            column_names = [i[0] for i in cursor.description]
            if get_result:
                if is_paginated:
                    cursor.execute('SELECT found_rows()')
                    found_rows = cursor.fetchall()
                    setattr(cls, 'total_count', found_rows[0][0])
                return [dict(zip(column_names, r)) for r in results]
        return lastrowid

    @classmethod
    def get_one(cls, query, params=()):
        cls.query_type = 'db_query'
        result = cls.process_query(query, params)
        if result and len(result) > 1:
            raise Exception("Multiple rows returned for database.get_one() query")
        return result[0] if result else None

    @classmethod
    def call_proc(cls, proc_name, params=()):
        # cls.query_type = 'db_query'
        with cls.transaction() as cursor:
            cursor.callproc(proc_name, params)
            column_names = [i[0] for i in cursor.description]
            more = True
            while more:
                results = cursor.fetchall()
                # Do something with these results
                more = cursor.nextset()
                return [dict(zip(column_names, r)) for r in results]

    @classmethod
    def as_dict(cls, results, pk=None):
        if pk is None:
            pk = cls.pk()
        return {item[pk]: item for item in results}

    @classmethod
    def get_id(cls, id):
        cls.query_type = 'db_query'
        sql = 'SELECT * FROM {} WHERE {} = {}'.format(cls.TABLE, cls.pk(), id)
        try:
            result = cls.process_query(sql)
        except MySQLdb.OperationalError:
            result = None
        if result and len(result) > 1:
            raise Exception("Multiple rows returned for database.get_id() query")
        return result[0] if result else None

    @classmethod
    def get_all(cls, order_by=None):
        cls.query_type = 'db_query'
        if order_by is None:
            order_by = ' create_dttm DESC'
        sql = "SELECT * FROM {} WHERE delete_dttm IS NULL ORDER BY {}".format(cls.TABLE, order_by)
        return cls.process_query(sql)

    @classmethod
    def get_recent(cls, limit=100):
        cls.query_type = 'db_query'
        sql = "SELECT * FROM {} WHERE delete_dttm IS NULL ORDER BY create_dttm DESC LIMIT %s".format(cls.TABLE)
        return cls.process_query(sql, (limit,))

    @classmethod
    def get_page(cls, page=1, per_page=20):
        cls.query_type = 'db_query'
        sql = "SELECT * FROM {} WHERE delete_dttm IS NULL ORDER BY create_dttm DESC LIMIT %s OFFSET %s".format(cls.TABLE)
        return cls.process_query(sql, (per_page, (page - 1) * per_page))

    @classmethod
    def delete(cls, item_id, audit_profile_id=None):
        cls.query_type = 'db_update'
        if audit_profile_id:
            sql = 'UPDATE {} SET delete_dttm=now(), audit_profile_id={} WHERE {} = %s'.format(cls.TABLE, audit_profile_id, cls.pk())
        else:
            sql = 'UPDATE {} SET delete_dttm=now() WHERE {} = %s'.format(cls.TABLE, cls.pk())
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s %s" % (sql, item_id))
            cursor.execute(sql, (item_id, ))

    @classmethod
    def delete_user(cls, id, user_id):
        cls.query_type = 'db_update'
        sql = 'UPDATE {} SET delete_dttm=now() WHERE {} = {} and user_id = {}'.format(
            cls.TABLE, cls.pk(), id, user_id)
        sql2 = 'update user set {} = null where user_id = {}'.format(cls.pk(), user_id)
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s" % sql)
            cursor.execute(sql)
            logging.debug("SQL query: %s" % sql2)
            cursor.execute(sql2)

    @classmethod
    def undelete(cls, id):
        cls.query_type = 'db_update'
        sql = 'UPDATE {} SET delete_dttm=null WHERE {} = {}'.format(
            cls.TABLE, cls.pk(), id)
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s" % sql)
            cursor.execute(sql)

    @classmethod
    def execute(cls, sql, *values):
        cls.query_type = 'db_update'
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s %s" % (sql, values))
            cursor.execute(sql, values)
            return cursor.lastrowid

    @classmethod
    def execute_no_values(cls, sql):
        cls.query_type = 'db_update'
        with cls.transaction() as cursor:
            logging.debug("SQL query: %s" % sql)
            cursor.execute(sql)
            return cursor.lastrowid

    @staticmethod
    def dict_to_where(attrs, joiner="AND"):
        """
        Convert a dictionary of attribute: value to a where statement.
        For example, dict_to_where({'one': 'two', 'three': 'four'}) returns:
        ['(one = ?) AND (three = ?)', 'two', 'four']

        >>> dict_to_where({'user_id': 100, 'first_name': 'Benjamin'})
        ['(first_name = %s) AND (user_id = %s)', 'Benjamin', 100]

        >>> dict_to_where({'is_active': None, 'first_name': 'Benjamin'})
        ['(first_name = %s) AND (is_active IS NULL)', 'Benjamin']
        """

        if len(attrs) == 0:
            return None

        wheres = []
        params = []
        for key, value in attrs.items():
            if value in (None, False):
                where = "(%s IS NULL)" % key
                del attrs[key]
            elif value is True:
                where = "(%s IS NOT NULL)" % key
                del attrs[key]
            elif isinstance(value, list):
                where = "(%s IN (%s))" % (key, ', '.join(['%s'] * len(value)))
                params.extend(value)
            else:
                where = "(%s = %%s)" % key
                params.append(value)
            wheres.append(where)
        return [(" %s " % joiner).join(wheres)] + params

    @staticmethod
    def prepare_in_query(field, values, exclude=False):
        """ Returns subquery for IN or NOT IN statement, ready to insert to a full query.

            Args:
                field (str): name of the field being searched
                values (list, tuple): list of values to be passed into IN statement
                exclude (bool): If True, returns a NOT IN statement, otherwise IN

            Return:
                Subquery ("field [NOT] IN (%s, %s, %s, ...)") in string form.
        """
        template = "{} NOT IN ({})" if exclude else "{} IN ({})"
        return template.format(field, ', '.join(['%s'] * len(values)))


class OrderedListMixin(object):
    @classmethod
    def swap_items(cls, item1, item2):
        cls.update({cls.pk(): item1[cls.pk()]}, order_nbr=item2['order_nbr'])
        cls.update({cls.pk(): item2[cls.pk()]}, order_nbr=item1['order_nbr'])

    @classmethod
    def move_up(cls, item_id):
        item = cls.get_id(item_id)
        if item:
            query = """
                SELECT {}, order_nbr
                FROM {}
                WHERE order_nbr < %s AND delete_dttm IS NULL
                ORDER BY order_nbr DESC
            """.format(cls.pk(), cls.TABLE)
            item_to_swap = cls.process_query(query, (item['order_nbr'], ))
            if item_to_swap:
                cls.swap_items(item, item_to_swap[0])

    @classmethod
    def move_down(cls, item_id):
        item = cls.get_id(item_id)
        if item:
            query = """
                SELECT {}, order_nbr
                FROM {}
                WHERE order_nbr > %s AND delete_dttm IS NULL
                ORDER BY order_nbr
            """.format(cls.pk(), cls.TABLE)
            item_to_swap = cls.process_query(query, (item['order_nbr'], ))
            if item_to_swap:
                cls.swap_items(item, item_to_swap[0])
