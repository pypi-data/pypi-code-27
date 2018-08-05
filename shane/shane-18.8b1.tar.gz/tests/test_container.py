import pytest
from pathlib import Path

import shane
from shane._container import Container


BASE = Path(__file__).parent
SAMPLES = BASE / "samples"
CONTAINERS_DIR = SAMPLES / "containers"


INFO_ATTRIBUTES = {
    "path",
    "extention",
    "format",
    "size",
    "bitrate",
    "duration",
    "start_time",
}

STREAM_ATTRIBUTES = {
    "streams",
    "audios",
    "videos",
    "subtitles",
    "data",
    "attachments",
    "images",
}

DEFAULT_ATTRIBUTES = {
    "default_path", 
    "default_extention",
}


@pytest.fixture
def containers():
    return {
        "mkv": shane.open(CONTAINERS_DIR / "mkv_container.mkv"),
        "m4v": shane.open(CONTAINERS_DIR / "m4v_container.m4v"),
        "avi": shane.open(CONTAINERS_DIR / "avi_container.avi"),
    }


def test_open_container(containers):
    for container in containers.values():
        assert isinstance(container, Container)


def test_default_values_contain_the_same(containers):
    for attr in INFO_ATTRIBUTES:
        for d_attr in DEFAULT_ATTRIBUTES:
            if attr in d_attr:
                for x in containers.values():
                    assert getattr(x, attr) == getattr(x, d_attr)


def test_create_empty_container(containers):
    empty_container = shane.Container()
    for attr in INFO_ATTRIBUTES | DEFAULT_ATTRIBUTES:
        assert getattr(empty_container, attr) is None
    for attr in STREAM_ATTRIBUTES:
        assert getattr(empty_container, attr) == ()



# def test_change_path_and_save(containers):
#     pass


# def test_change_extention_and_save():
#     pass


# def test_change_global_metadata_and_save():
#     pass


# def test_add_stream_and_save():
#     pass


# def test_remove_stream_and_save():
#     pass


# def test_remove_stream_if_some_condition_and_save():
#     pass