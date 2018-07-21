
import json
import re

import bottle
import jsonschema
from bottle import abort, request

class SchemaValidationError(bottle.HTTPError):
    def __init__(self, errors):
        self.validation_errors = errors

        body = json.dumps({
            "error": "payload failed json schema validation",
            "validation_errors": errors,
        })

        super(SchemaValidationError, self).__init__(400, body, headers={
            "Content-Type": "application/json"
        })

class JSONSchemaPlugin:
    """This plugin automatically validates JSON payloads using JSON schemas"""

    name = "jsonschema"
    api = 2

    def __init__(self, schema_lookup=None, schema_name=None,
                 methods=("POST", "PATCH", "PUT")):
        self.schema_lookup = (schema_lookup or self._fetch_schema)
        self.schema_name = (schema_name or self._get_schema_names)
        self.methods = methods

    def setup(self, app):
        self.app = app

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            if route.method in self.methods:
                self._validate_schema()

            return callback(*args, **kwargs)

        return wrapper

    def _validate_schema(self):
        schema = self.schema_lookup()

        if schema:
            if request.content_type != "application/json":
                abort(400, "content type application/json required")

            try:
                payload = request.json
            except json.JSONDecodeError:
                abort(400, "json payload could not be parsed")

            if payload is None:
                abort(400, "json payload required")

            errors = self._validate_payload(schema, payload)

            if len(errors) > 0:
                raise SchemaValidationError(errors)

    def _get_schema_names(self, rule=None, method=None):
        """Returns a list of possible schema names for the current route"""

        if not rule:
            rule = request.route.rule

        if not method:
            method = request.method

        rule = rule.strip("/")
        rule = rule.replace("/", ".")
        rule = re.sub(r"<(\w+)(:.*?)?>", r"\1", rule)

        return [
            "schemas/{}.{}.json".format(rule, method),
            "schemas/{}.json".format(rule),
        ]

    def _fetch_schema(self):
        """Finds and returns the appropriate JSON schema for the input route

        Returns None if no schema could be found.
        """

        attempts = self.schema_name()

        for path in attempts:
            try:
                with self.app.resources.open(path) as f:
                    return json.loads(f.read())
            except IOError:
                next

        return None

    def _validate_payload(self, schema, payload):
        """Validates the payload and returns a list of errors"""

        validator = jsonschema.validators.validator_for(schema)(schema)

        errors = [
            "failed constraint: {}: {}".format(
                ".".join(error.schema_path),
                error.validator_value,
            )
            for error in validator.iter_errors(payload)
        ]

        return list(set(errors))
