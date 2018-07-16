import mock
import pytest

from hermes_python.hermes import Hermes

HOST = "localhost"


def test_initialization():
    h = Hermes(HOST)
    assert 0 == len(h._c_callback_subscribe_intent)


@mock.patch("hermes_python.hermes.lib")
def test_context_manager_enter(mocked_lib):
    with Hermes(HOST) as h:
        pass

    mocked_lib.hermes_protocol_handler_new_mqtt.assert_called_once()
    mocked_lib.hermes_protocol_handler_dialogue_facade.assert_called_once()


@mock.patch("hermes_python.hermes.hermes_drop_dialogue_facade")
@mock.patch("hermes_python.hermes.lib")
def test_context_manager_exit(mocked_lib, mocked_hermes_drop_dialogue_facade):
    with Hermes(HOST) as h:
        pass
    mocked_hermes_drop_dialogue_facade.assert_called_once()


@mock.patch("hermes_python.hermes.hermes_drop_dialogue_facade")
@mock.patch("hermes_python.hermes.lib")
def test_context_manager_catches_exceptions(mocked_lib, mocked_hermes_drop_dialogue_facade):
    mocked_lib.hermes_protocol_handler_dialogue_facade.side_effect = Exception("An exception occured!")

    with pytest.raises(Exception):
        with Hermes(HOST) as h:
            pass


