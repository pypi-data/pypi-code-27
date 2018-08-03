import os
import pytest
from vcap_services import load_from_vcap_services


dummy_creds = {'username': 'Mo', 'password': 'Salah'}

def test_vcap_services_not_none():
    assert load_from_vcap_services('assistant') == dummy_creds
    assert load_from_vcap_services('discovery') is None

def test_service_label_in_env():
    assert load_from_vcap_services('speech_to_text', 'lite', 'stt') == dummy_creds

def test_service_label_in_env_catch_error():
    with pytest.raises(KeyError):
        load_from_vcap_services('speech_to_text', 'lite', 'stt_wrong')

def test_vcap_services_is_none():
    del os.environ['VCAP_SERVICES']
    assert load_from_vcap_services('assistant') is None
