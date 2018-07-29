from inspect import signature
from typing import Callable

import colander

from pyramid_request_schema.base_schema import RequestSchema
from pyramid_request_schema.exceptions import RequestSchemaInvalid


def schema_validated_view(view: Callable, info):
    concrete_request_schema_cls = info.options.get("request_schema", None)

    if concrete_request_schema_cls:
        concrete_request_schema = concrete_request_schema_cls()
        view_signature = signature(view)
        takes_context = len(view_signature.parameters) == 2

        def wrapper_view(request_or_context, maybe_request=None):
            if maybe_request is None:
                request = request_or_context
                context = None
            else:
                request = maybe_request
                context = request_or_context

            abstract_request_schema = RequestSchema()

            try:
                request_data = abstract_request_schema.serialize(request)
                validated = concrete_request_schema.deserialize(request_data)
            except colander.Invalid as e:
                raise RequestSchemaInvalid(e)

            setattr(request, "validated", validated)

            if takes_context:
                return view(context, request)

            return view(request)

        return wrapper_view

    return view


schema_validated_view.options = ("request_schema", )
