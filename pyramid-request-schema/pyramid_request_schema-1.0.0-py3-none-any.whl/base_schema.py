from json import JSONDecodeError

import colander
from colander import Invalid
from pyramid.interfaces import IRequest
from pyramid.request import Request


class RequestSchema(colander.MappingSchema):
    body = colander.SchemaNode(colander.Mapping(unknown="preserve"))
    queryset = colander.SchemaNode(colander.Mapping(unknown="preserve"))

    def serialize(self, appstruct: Request):
        if appstruct is colander.null:
            return colander.null

        if not IRequest.providedBy(appstruct):
            msg = '{:s} does not implement IRequest interface'.format(
                str(appstruct))
            raise Invalid(self, msg)

        content_type = getattr(appstruct,
                               "content_type",
                               "application/octet-stream")

        if content_type != "application/json":
            msg = "{:s} is not a json request.".format((str(appstruct)))
            raise Invalid(self, msg)

        try:
            json_body = appstruct.json_body or {}
        except (JSONDecodeError, AttributeError):
            json_body = {}

        appstruct = {
            "body": json_body,
            "queryset": appstruct.GET,
        }

        return super(RequestSchema, self).serialize(appstruct)

    def deserialize(self, node, cstruct):
        raise NotImplementedError()
