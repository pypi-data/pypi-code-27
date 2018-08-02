import json

from django.db import models
from django.contrib.postgres.fields import JSONField


class AgnosticJSONField(models.Field):

    """
    AgnosticJSONField


    :usage

       field_name = AgnosticJSONField()

    """

    def __init__(self, encoder=None, *args, **kwargs):
        self.encoder = encoder
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['encoder'] = self.encoder
        return name, path, args, kwargs

    def _get_field(self, connection):
        if (connection.settings_dict['ENGINE'] ==
                'django.db.backends.postgresql_psycopg2'):
            if self.encoder:
                return JSONField(encode=self.encoder)
            return JSONField()
        return models.TextField()

    def db_type(self, connection):
        field = self._get_field(connection)
        return field.db_type(connection)

    def get_db_prep_save(self, value, connection):
        """
        get_db_prep_save is called when saving data to a database.
        For pg, save it as a json.
        For other engines, save it as a string in form of a
        json dump
        """
        field = self._get_field(connection)
        if isinstance(field, JSONField):
            return field.get_db_prep_save(value, connection)
        else:
            new_value = json.dumps(value, cls=self.encoder)
            return new_value

    def from_db_value(self, value, expression, connection):
        """
        from_db_value is called when retriving data from database.
        For pg,retrieve data as a array
        For other engines, retrive the data which will be returned as
        as json string,then convert it to a dict object
        """
        field = self._get_field(connection)
        if isinstance(field, JSONField):
            return value
        else:
            new_value = json.loads(value)
            return new_value
