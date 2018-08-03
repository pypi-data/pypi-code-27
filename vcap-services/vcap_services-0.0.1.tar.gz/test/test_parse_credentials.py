from vcap_services import parse_credentials

dummy_file_creds = {'watson_discovery_username': 'Leo', 'watson_discovery_password': 'Messi', 'some_other_password': 'Ramos'}
dummy_file_parsed = {'username': 'Leo', 'password': 'Messi'}

def test_empty_dict():
    assert parse_credentials('assistant', {}) == {}

def test_dummy_config():
    assert parse_credentials('discovery', dummy_file_creds) == dummy_file_parsed
    assert parse_credentials('discovery', {}) == {}
