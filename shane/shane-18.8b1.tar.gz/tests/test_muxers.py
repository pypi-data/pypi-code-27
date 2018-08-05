import pytest
from pathlib import Path

import shane
import os
from shane.muxers import m4v, mkv


BASE = Path(__file__).parent
SAMPLES = BASE / "samples"
CONTAINERS_DIR = SAMPLES / "containers"


def teardown_function():
    for container_path in CONTAINERS_DIR.glob("*"):
        if container_path.suffix.replace('.', '') not in container_path.stem:
            os.remove(container_path)


def public_info_attr(attr, container):
    """Returns True if `container.attr` is 
        - not callable
        - not returns tuple of streams
        - not starts with '_'."""
    if attr.startswith('_'):
        return False
    if callable(getattr(container, attr)):
        return False
    if isinstance(getattr(container, attr), tuple):
        return False
    return True


def test_mkv_muxer():
    avi_container = shane.open(CONTAINERS_DIR / "avi_container.avi")
    m4v_container = shane.open(CONTAINERS_DIR / "m4v_container.m4v")

    assert Path(avi_container.path).with_suffix(".mkv").exists() == False
    assert Path(m4v_container.path).with_suffix(".mkv").exists() == False
    
    returned_mkv_from_avi_container = mkv(avi_container)
    returned_mkv_from_m4v_container = mkv(m4v_container)

    assert Path(avi_container.path).with_suffix(".mkv").exists() == True
    assert Path(m4v_container.path).with_suffix(".mkv").exists() == True

    assert returned_mkv_from_avi_container.extention == ".mkv"
    assert returned_mkv_from_m4v_container.extention == ".mkv"

    opened_mkv_from_avi_container = shane.open(
        CONTAINERS_DIR / "avi_container.mkv"
    )
    opened_mkv_from_m4v_container = shane.open(
        CONTAINERS_DIR / "m4v_container.mkv"
    )

    for attr in dir(opened_mkv_from_avi_container):
        if public_info_attr(attr, opened_mkv_from_avi_container):
            assert getattr(opened_mkv_from_avi_container, attr) == \
            getattr(returned_mkv_from_avi_container, attr)
    
    for attr in dir(opened_mkv_from_m4v_container):
        if public_info_attr(attr, opened_mkv_from_m4v_container):
            assert getattr(opened_mkv_from_m4v_container, attr) == \
            getattr(returned_mkv_from_m4v_container, attr)



def test_m4v_muxer():
    avi_container = shane.open(CONTAINERS_DIR / "avi_container.avi")
    mkv_container = shane.open(CONTAINERS_DIR / "mkv_container.mkv")
    
    assert Path(avi_container.path).with_suffix(".m4v").exists() == False
    assert Path(mkv_container.path).with_suffix(".m4v").exists() == False

    returned_m4v_from_avi_container = m4v(avi_container)
    returned_m4v_from_mkv_container = m4v(mkv_container)

    assert Path(avi_container.path).with_suffix(".m4v").exists() == True
    assert Path(mkv_container.path).with_suffix(".m4v").exists() == True

    assert returned_m4v_from_avi_container.extention == ".m4v"
    assert returned_m4v_from_mkv_container.extention == ".m4v"


    opened_m4v_from_avi_container = shane.open(
        CONTAINERS_DIR / "avi_container.m4v"
    )
    opened_m4v_from_mkv_container = shane.open(
        CONTAINERS_DIR / "mkv_container.m4v"
    )

    for attr in dir(opened_m4v_from_avi_container):
        if public_info_attr(attr, opened_m4v_from_avi_container):
            assert getattr(opened_m4v_from_avi_container, attr) == \
            getattr(returned_m4v_from_avi_container, attr)
    
    for attr in dir(opened_m4v_from_mkv_container):
        if public_info_attr(attr, opened_m4v_from_mkv_container):
            assert getattr(opened_m4v_from_mkv_container, attr) == \
            getattr(returned_m4v_from_mkv_container, attr)