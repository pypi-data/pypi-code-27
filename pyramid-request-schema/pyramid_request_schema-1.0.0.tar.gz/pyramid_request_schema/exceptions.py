import colander
from pyramid.httpexceptions import HTTPBadRequest


class RequestSchemaInvalid(HTTPBadRequest):
    content_type = "application/json"

    def __init__(self, colander_exception: colander.Invalid, *args, **kwargs):
        self.colander_exception = colander_exception
        super(RequestSchemaInvalid, self).__init__(*args, **kwargs)

        self.json_body = {
            "errors": self.colander_exception.asdict()
        }
