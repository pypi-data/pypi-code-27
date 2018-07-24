import pytest
import responses

from en16931 import validex


api_key='6df3de0197ee4f9a8b296c51dcc54a5c'
user_id=5


def test_validex_success(invoice1):
    validex_success_json = {'report': {'documentHash': '933098de',
        'documentTypes': [{'criteria': [{'expression': "(contains(namespace-uri(), 'urn:oasis:names:specification:ubl:schema:xsd') and ends-with(namespace-uri(), '2'))",
            'expressionType': 'xpath'}],
            'matches': True,
            'name': 'UBL 2',
            'path': 'doc/xml/ubl2',
            'subStart': True},
            {'criteria': [{'expression': "namespace-uri() = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'",
                'expressionType': 'xpath'}],
                'matches': True,
                'name': 'Invoice',
                'path': 'doc/xml/ubl2/inv',
                'subStart': False}],
            'duration': 0.47534894943237,
            'filename': '1531216744.xml',
            'id': 'ljc7yi',
            'result': 'success',
            'success': True,
            'timestamp': '2018-07-10T10:06:09+00:00',
            'userId': 5,
            'validationSteps': [{'description': 'XML Structural Validation',
                'documentType': 'doc/xml',
                'errors': [],
                'name': 'xml-structure',
                'success': True,
                'validationType': 'xml'},
                {'description': 'UBL 2.1 Invoice',
                    'documentType': 'doc/xml/ubl2/inv',
                    'errors': None,
                    'name': 'ubl-2_1-invoice-schema',
                    'success': True,
                    'validationType': 'schema'}]}} 
    responses.add(responses.POST, 'https://api2.validex.net/api/validate',
                  json=validex_success_json, status=200)
    assert validex.is_valid_at_validex(invoice1, api_key, user_id)


def test_validex_fail(invoice1):
    validex_success_json = {'report': {'documentHash': '933098de',
        'documentTypes': [{'criteria': [{'expression': "(contains(namespace-uri(), 'urn:oasis:names:specification:ubl:schema:xsd') and ends-with(namespace-uri(), '2'))",
            'expressionType': 'xpath'}],
            'matches': True,
            'name': 'UBL 2',
            'path': 'doc/xml/ubl2',
            'subStart': True},
            {'criteria': [{'expression': "namespace-uri() = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'",
                'expressionType': 'xpath'}],
                'matches': True,
                'name': 'Invoice',
                'path': 'doc/xml/ubl2/inv',
                'subStart': False}],
            'duration': 0.47534894943237,
            'filename': '1531216744.xml',
            'id': 'ljc7yi',
            'result': 'fatal',
            'success': True,
            'timestamp': '2018-07-10T10:06:09+00:00',
            'userId': 5,
            'validationSteps': [{'description': 'XML Structural Validation',
                'documentType': 'doc/xml',
                'errors': [],
                'name': 'xml-structure',
                'success': True,
                'validationType': 'xml'},
                {'description': 'UBL 2.1 Invoice',
                    'documentType': 'doc/xml/ubl2/inv',
                    'errors': None,
                    'name': 'ubl-2_1-invoice-schema',
                    'success': True,
                    'validationType': 'schema'}]}} 
    responses.add(responses.POST, 'https://api2.validex.net/api/validate',
                  json=validex_success_json, status=200)
    assert validex.is_valid_at_validex(invoice1, api_key, user_id)
