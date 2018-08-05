import pytest

import shane
from shane._streams import *

BASE = Path(__file__).parent
SAMPLES = BASE / "samples"
STREAMS_DIR = SAMPLES / "streams"


@pytest.fixture
def streams():
    return {
        "aac": shane.open(STREAMS_DIR / "aac_audio.aac"),
        "ac3": shane.open(STREAMS_DIR / "ac3_audio.ac3"),
        "srt": shane.open(STREAMS_DIR / "srt_subtitles.srt"),
    }


def test_stream_of_correct_class(streams):
    assert isinstance(streams["aac"], AudioStream)
    assert isinstance(streams["ac3"], AudioStream)
    assert isinstance(streams["srt"], SubtitleStream)
