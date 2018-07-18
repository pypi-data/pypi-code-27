from typing import Type

from longitude.models.sql import SQLCRUDModel
from marshmallow import Schema as OriginalSchema, fields, validates_schema
from sanic.request import RequestParameters

from .validators import validate_obj_attr_uniqueness, validate_obj_attr_existence


def bind_uniqueness_schema_validator(schema, field_name):

    def validate(self, data):
        if getattr(self, 'model', None) is None:
            raise RuntimeError('To bind a uniqueness validator, please pass a model to the schema.')

        field_value = data.get(field_name, None)
        obj_id = data.get('id', None)

        if field_value is not None:
            validate_obj_attr_uniqueness(self.model, obj_id, field_name, field_value)

    validator = validates_schema(validate)
    validator_name = '_validate_{}_uniqueness'.format(field_name)
    _add_processor_to_schema(schema, validator_name, validator)


def bind_fkexists_schema_validator(
    schema,
    field_name,
    foreign_model_class: Type[SQLCRUDModel],
    extra_filters_attr=None
):

    def validate(self: ModelSchema, data):
        if getattr(self, 'model', None) is None:
            raise RuntimeError('To bind a fkexists validator, please pass a model to the schema.')

        fk = data.get(field_name, None)

        extra_filters = getattr(self, extra_filters_attr) \
            if extra_filters_attr else {}

        foreign_model = self._model_cache.get(
            (foreign_model_class.__module__, foreign_model_class.__name__),
            None
        )

        if foreign_model is None:
            foreign_model = foreign_model_class(self.model.db_model, self.model.db_conn)
            self._model_cache[(foreign_model_class.__module__, foreign_model_class.__name__)] = \
                foreign_model

        if fk is not None:
            validate_obj_attr_existence(foreign_model, field_name, fk, extra_filters=extra_filters)

    validator = validates_schema(validate)
    validator_name = '_validate_{}_fkexists'.format(field_name)
    _add_processor_to_schema(schema, validator_name, validator)


def _add_processor_to_schema(schema, name, fn):
    setattr(schema, name, fn)
    for tag in fn.__marshmallow_tags__:
        schema.__processors__[tag].insert(0, name)


class Schema(OriginalSchema):
    def load(self, data, many=None, partial=None):
        # Request stores parameters as list (to deal with
        # param duplication). This feature interferes with
        # direct usage of request parameters in load method
        if isinstance(data, RequestParameters):
            data = {
                x: data.get(x)
                for x
                in data.keys()
                if x not in ('token_payload', 'sql_conn')
            }

        return super().load(data, many, partial)


class ModelSchema(Schema):

    id = fields.Integer(
        required=False
    )

    # Used by helper functions to store
    # schema instances that may be used
    # among different bindable validators, like
    # bind_fkexists_schema_validator
    _model_cache = {}

    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model
