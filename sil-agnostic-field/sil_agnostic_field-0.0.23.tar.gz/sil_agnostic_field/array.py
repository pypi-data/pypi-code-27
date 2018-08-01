import json

from django.contrib.postgres.fields import ArrayField
from django.db.models.lookups import Exact, In

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from . import lookup
from .util import check_if_pg_connection


class AgnosticArrayField(models.Field):
    """
    AgnosticArrayField serializes array values without
    reliant to a specific database engine.The goal is to
    allow array storage and retrived on any django
    supported database engine

    :usage

       field_name = AgnosticArrayField(models.TextField(max_length=255))

    :creation
        ModelName.objects.create(field_name=['array','items','here'])

    :lookup
        ModelName.objects.filter(field_name__contains=['identifier'])

    """

    def __init__(self, base_field, size=None, *args, **kwargs):
        self.base_field = base_field
        self.size = size
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['base_field'] = self.base_field
        kwargs['size'] = self.size
        return name, path, args, kwargs

    def _get_field(self, connection):
        if check_if_pg_connection():
            return ArrayField(self.base_field, self.size)
        return models.TextField()

    def db_type(self, connection):
        field = self._get_field(connection)
        return field.db_type(connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        get_db_prep_value is called when saving value to database.
        For pg, save the value as an array.
        For other engines, convert the value to a pickle dump
        """
        field = self._get_field(connection)
        if isinstance(field, ArrayField):
            return field.get_db_prep_value(value, connection, prepared)
        else:
            if value:
                return json.dumps(value, cls=DjangoJSONEncoder)
            return None

    def from_db_value(self, value, expression, connection):
        """
        from_db_value is called when retriving data from database.
        For pg,retrieve data as a array
        For other engines, retrive the data which will be returned as
        as pickle dump,then convert it to a list object
        """
        field = self._get_field(connection)
        if isinstance(field, ArrayField):
            return value
        else:
            if value:
                return json.loads(value)
            return None


@AgnosticArrayField.register_lookup
class ArrayContains(lookup.DataContains):
    def as_sql(self, qn, connection):
        if check_if_pg_connection():
            sql, params = super().as_sql(qn, connection)
            sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
            return sql, params
        sql, params = super().as_sql(qn, connection)
        lite = []
        for p in params[0]:
            n = '%{}%'.format(p)
            lite.append(n)
        return sql, lite


@AgnosticArrayField.register_lookup
class ArrayContainedBy(lookup.ContainedBy):
    def as_sql(self, qn, connection):
        sql, params = super().as_sql(qn, connection)
        sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
        return sql, params


@AgnosticArrayField.register_lookup
class ArrayExact(Exact):
    def as_sql(self, qn, connection):
        if check_if_pg_connection():
            sql, params = super().as_sql(qn, connection)
            sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
            return sql, params
        sql, params = super().as_sql(qn, connection)
        sql = '%s' % (sql)
        return sql, params


@AgnosticArrayField.register_lookup
class ArrayOverlap(lookup.Overlap):

    def as_sql(self, qn, connection):
        if check_if_pg_connection():
            sql, params = super().as_sql(qn, connection)
            sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
            return sql, params
        sql, params = super().as_sql(qn, connection)

        lite = []
        for p in params[0]:
            n = '%{}%'.format(p)
            lite.append(n)

        if len(lite) == 1:
            return sql, lite
        elif len(lite) == 2:
            field = sql.split('.')[1].split(' ')[0]
            n = [sql, 'OR', field, 'LIKE %s']
            sql = n[0] + ' ' + n[1] + ' ' + n[2] + ' ' + n[3]
            return sql, lite
        elif len(lite) == 3:
            field = sql.split('.')[1].split(' ')[0]
            n = [sql, 'OR', field, 'LIKE %s', 'OR', field, 'LIKE %s']
            sql = n[0] + ' ' + n[1] + ' ' + n[2] + ' ' + \
                n[3] + ' ' + n[4] + ' ' + n[5] + ' ' + n[6]
            return sql, lite
        elif len(lite) == 4:
            field = sql.split('.')[1].split(' ')[0]
            n = [sql, 'OR', field, 'LIKE %s', 'OR', field, 'LIKE %s', 'OR', field, 'LIKE %s']
            sql = n[0] + ' ' + n[1] + ' ' + n[2] + ' ' + n[3] + ' ' + n[4] + \
                ' ' + n[5] + ' ' + n[6] + ' ' + n[7] + ' ' + n[8] + ' ' + n[9]
            return sql, lite


@AgnosticArrayField.register_lookup
class ArrayLenTransform(models.Transform):
    lookup_name = 'len'
    output_field = models.IntegerField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        # Distinguish NULL and empty arrays
        return (
            'CASE WHEN %(lhs)s IS NULL THEN NULL ELSE '
            'coalesce(array_length(%(lhs)s, 1), 0) END'
        ) % {'lhs': lhs}, params


@AgnosticArrayField.register_lookup
class ArrayInLookup(In):
    def get_prep_lookup(self):
        values = super().get_prep_lookup()
        if hasattr(self.rhs, '_prepare'):
            # Subqueries don't need further preparation.
            return values
        # In.process_rhs() expects values to be hashable, so convert lists
        # to tuples.
        prepared_values = []
        for value in values:
            if hasattr(value, 'resolve_expression'):
                prepared_values.append(value)
            else:
                prepared_values.append(tuple(value))
        return prepared_values
