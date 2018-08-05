from pathlib import Path

import pytest

from shane._ffmpeg import FFprobe


BASE = Path(__file__).parent
SAMPLES = BASE / "samples"
CONTAINERS_DIR = SAMPLES / "containers"


@pytest.fixture(scope="module")
def ffprobe():
    path = CONTAINERS_DIR / "mkv_container.mkv"
    return FFprobe(path)


def test_get_all_keys(ffprobe):
    data = ffprobe.get_all()
    assert isinstance(data, dict)
    assert "streams" in data
    assert "chapters" in data
    assert "format" in data


def test_getting_streams(ffprobe):
    data = ffprobe.get_streams()
    assert isinstance(data, list)
    assert isinstance(data[0], dict)


def test_getting_chapters(ffprobe):
    data = ffprobe.get_chapters()
    assert isinstance(data, list)


def test_getting_format(ffprobe):
    data = ffprobe.get_format()
    assert isinstance(data, dict)
