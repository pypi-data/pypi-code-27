import os
import json
from vcap_services import get_credentials_from_file

dummy_VCAP_creds = {'username': 'Mo', 'password': 'Salah'}
dummy_file_creds = {'watson_discovery_username': 'Leo', 'watson_discovery_password': 'Messi', 'some_other_password': 'Ramos'}
dummy_file_parsed = {'username': 'Leo', 'password': 'Messi'}
dummy_kube_creds = {'apikey': 'cr7', 'url':'fifa'}

def test_VCAP_creds():
    assert get_credentials_from_file('assistant') == dummy_VCAP_creds

def test_no_file():
    assert get_credentials_from_file('discovery') == {}

def test_creds_from_file():
    assert get_credentials_from_file('discovery', dummy_file_creds) == dummy_file_parsed
    assert get_credentials_from_file('discovery', {}) == {}

def test_kube_creds():
    os.environ['service_watson_visual_recognition'] = json.dumps(dummy_kube_creds)
    assert get_credentials_from_file('visual_recognition') == dummy_kube_creds
    del os.environ['service_watson_visual_recognition']
