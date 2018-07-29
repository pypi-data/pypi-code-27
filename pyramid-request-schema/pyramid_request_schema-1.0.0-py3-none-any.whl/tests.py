from unittest import TestCase
from unittest.mock import Mock
from pyramid import testing
import colander
from pyramid_request_schema.deriver import RequestSchema, schema_validated_view
from pyramid_request_schema.exceptions import RequestSchemaInvalid


class TestBodyRequestSchema(colander.MappingSchema):

    @colander.instantiate()
    class body(colander.MappingSchema):
        str_val = colander.SchemaNode(colander.String())
        float_val = colander.SchemaNode(colander.Float())


class TestQSRequestSchema(colander.MappingSchema):

    @colander.instantiate()
    class queryset(colander.MappingSchema):
        str_val = colander.SchemaNode(colander.String())
        float_val = colander.SchemaNode(colander.Float())


class SerializationTests(TestCase):

    def test_correct_request_serialization(self):
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={"str_val": "val1",
                                                  "float_val": "2.3"})
        request_data = RequestSchema().serialize(request)

        self.assertIsInstance(request_data, dict)
        self.assertIn("str_val", request_data["body"])
        self.assertIn("float_val", request_data["body"])

        self.assertEqual("val1", request_data["body"]["str_val"])
        self.assertEqual("2.3", request_data["body"]["float_val"])

    def test_correct_queryset_serialization(self):
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={},
                                       params={"str_val": "val1",
                                               "float_val": "2.3"})
        request_data = RequestSchema().serialize(request)

        self.assertIsInstance(request_data, dict)
        self.assertIn("str_val", request_data["queryset"])
        self.assertIn("float_val", request_data["queryset"])

        self.assertEqual("val1", request_data["queryset"]["str_val"])
        self.assertEqual("2.3", request_data["queryset"]["float_val"])

    def test_incorrect_request_serialization(self):
        request = testing.DummyRequest(content_type="application/json",
                                       json_body="test")

        with self.assertRaises(colander.Invalid):
            RequestSchema().serialize(request)


class SchemaValidatedViewTests(TestCase):

    def base_view(self, request):
        self.assertTrue(hasattr(request, "validated"))
        return request.validated

    def setUp(self):
        self.info = Mock()
        self.info.options = {"request_schema": TestBodyRequestSchema}
        self.view = schema_validated_view(self.base_view, self.info)

    def test_correct_request_deserialization(self):
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={"str_val": "val1",
                                                  "float_val": "2.3"})
        validated = self.view(request)
        self.assertIsInstance(validated, dict)
        self.assertIn("str_val", validated["body"])
        self.assertIn("float_val", validated["body"])

        self.assertEqual("val1", validated["body"]["str_val"])
        self.assertEqual(2.3, validated["body"]["float_val"])

    def test_incorrect_request_deserialization_raises_400(self):
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={"float_val": "aaa"})

        with self.assertRaises(RequestSchemaInvalid) as e:
            self.view(request)

        self.assertIn("errors", e.exception.json_body)
        self.assertIn("body.str_val", e.exception.json_body["errors"])

    def context_is_not_none_view(self, context, request):
        self.assertIsNotNone(context)
        self.assertIsNotNone(request)

    def test_view_gets_context(self):
        view = schema_validated_view(self.context_is_not_none_view, self.info)
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={"str_val": "val1",
                                                  "float_val": "2.3"})
        context = testing.DummyResource()

        view(context, request)

    def context_is_not_accepted_view(self, request):
        self.assertIsNotNone(request)

    def test_view_gets_only_request(self):
        view = schema_validated_view(self.context_is_not_accepted_view, self.info)
        request = testing.DummyRequest(content_type="application/json",
                                       json_body={"str_val": "val1",
                                                  "float_val": "2.3"})
        context = testing.DummyResource()
        view(context, request)

    def test_queryset_only_validation(self):
        info = Mock()
        info.options = {"request_schema": TestQSRequestSchema}
        view = schema_validated_view(self.base_view, info)
        request = testing.DummyRequest(content_type="application/json",
                                       json_body="",
                                       params={"str_val": "val1",
                                                  "float_val": "2.3"})
        context = testing.DummyResource()
        view(context, request)
