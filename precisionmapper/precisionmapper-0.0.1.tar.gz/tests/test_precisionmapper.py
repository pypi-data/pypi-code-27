#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `precisionmapper` package."""

# To be tested with : python3 -m pytest -vs tests/test_precisionmapper.py

import pytest
import os
from precisionmapper import Survey, PrecisionMapper
from requests import ConnectionError

# Get useful environment variables
_LOGIN = os.environ.get('PRECISIONMAPPER_LOGIN', None)
_PASSWORD = os.environ.get('PRECISIONMAPPER_PASSWORD', None)


def test_class_Survey():
    survey = Survey(
        id=123, name="My survey", url="https://url.com",
        drone_platform="DJI",
        sensor="RGB", location="Toulouse, France",
        date="2018-08-03T17:00:00.001Z", image_nb=3, size="150 MB",
        thumbnail="https://url_to_thumbnail.com", altitude_in_m=90,
        resolution_in_cm=2.5, area_in_ha=1.8)
    assert survey.id == 123
    assert str(survey) == "[My survey] (Toulouse, France - 03/08/2018 17:00) \
: 3 images, 150 MB, sensor : RGB"
    assert repr(survey) == "Survey(id=123, name=My survey)"
    print()
    print(survey)

    # Test with the mandatory parameters only
    survey = Survey(
        id=456, name="My survey 2", url="https://url.com",
        date="2018-08-03T16:00:00.001Z")
    assert survey.id == 456
    assert str(survey) == "[My survey 2] ( - 03/08/2018 16:00) \
: 0 images, 0 MB, sensor : "
    print(survey)


def test_class_Survey_errors():
    with pytest.raises(TypeError):
        # Bad type for image number
        Survey(
            id=123, name="My survey", url="https://url.com",
            drone_platform="DJI",
            sensor="RGB", location="Toulouse, France",
            date="2018-08-03T17:00:00.001Z", image_nb="ABC", size="150 MB",
            thumbnail="https://url_to_thumbnail.com", altitude_in_m=90,
            resolution_in_cm=2.5, area_in_ha=1.8)

    with pytest.raises(TypeError):
        # Bad type for date
        Survey(
            id=123, name="My survey", url="https://url.com",
            drone_platform="DJI",
            sensor="RGB", location="Toulouse, France",
            date="not a date", image_nb=3, size="150 MB",
            thumbnail="https://url_to_thumbnail.com", altitude_in_m=90,
            resolution_in_cm=2.5, area_in_ha=1.8)

    with pytest.raises(TypeError):
        # Bad type for id
        Survey(
            id="abc", name="My survey 2", url="https://url.com",
            date="2018-08-03T16:00:00.001Z")


def test_class_PrecisionMapper():
    pm = PrecisionMapper(login="username", password="password")
    assert repr(pm) == "PrecisionMapper(login=username)"
    assert str(pm) == "PrecisionMapper(login=username)"


def test_get_authenticity_token():
    pm = PrecisionMapper(login=_LOGIN, password=_PASSWORD)
    authenticity_token = pm.get_authenticity_token()
    assert authenticity_token != ""
    print()
    print("authenticity_token = {}".format(authenticity_token))


def test_get_authenticity_token_errors():
    with pytest.raises(ValueError):
        # Bad type for image number
        pm = PrecisionMapper(login=_LOGIN, password=_PASSWORD)
        pm.get_authenticity_token(url="https://example.com")


def test_signin():
    pm = PrecisionMapper(login=_LOGIN, password=_PASSWORD)
    sign_in = pm.sign_in()
    assert sign_in.status_code == 302
    # Status code is 302 because there is a redirection when sign_in OK


def test_signin_errors():
    with pytest.raises(ConnectionError):
        # Bad login and password
        pm = PrecisionMapper(login="bad_login", password="bad_password")
        pm.sign_in()


def test_get_surveys():
    pm = PrecisionMapper(login=_LOGIN, password=_PASSWORD)
    pm.sign_in()
    surveys = pm.get_surveys()
    assert len(surveys) > 0
    assert type(surveys[0]) == Survey
    print()
    for survey in surveys:
        print(survey)


def test_get_shared_surveys():
    pm = PrecisionMapper(login=_LOGIN, password=_PASSWORD)
    pm.sign_in()
    surveys = pm.get_shared_surveys()
    assert len(surveys) > 0
    assert type(surveys[0]) == Survey
    print()
    for survey in surveys:
        print(survey)
