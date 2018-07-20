import capturer

import pytest

from distinfo import config


@pytest.fixture(autouse=True)
def logging():
    config.cfg.logging.config.isatty = True
    config.configure_logging()


class DummyCapture:

    def __init__(self, **_kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, _etype, _value, _tb):
        pass

    def get_text(self):
        return ""


# capturer doesn't like pytest, so dummy it out
@pytest.fixture(autouse=True)
def dummy_capture(monkeypatch):
    monkeypatch.setattr(capturer, "CaptureOutput", DummyCapture)
