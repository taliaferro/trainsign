import pytest
import os
import vcr
from .client import Open511Client


@pytest.fixture
def test_client():
    return Open511Client(api_key=os.getenv("TRAIN_SIGN_KEY"))


@pytest.mark.vcr()
def test_stop_monitoring(test_client):
    assert test_client.stop_monitoring("SF")


@pytest.mark.vcr()
def test_vehicle_monitoring(test_client):
    assert test_client.vehicle_monitoring("SF")


@pytest.mark.vcr()
def test_operators(test_client):
    assert test_client.operators()


@pytest.mark.vcr()
def test_lines(test_client):
    assert test_client.lines("SF")


@pytest.mark.vcr()
def test_stops(test_client):
    assert test_client.stops("SF")


@pytest.mark.vcr()
def test_stop_places(test_client):
    assert test_client.stop_places("SF")


@pytest.mark.vcr()
def test_patterns(test_client):
    assert test_client.patterns("SF", "KT")


@pytest.mark.vcr()
def test_timetable(test_client):
    assert test_client.timetable("SF", "KT")


@pytest.mark.vcr()
def test_stop_timetable(test_client):
    # I don't know how this endpoint works
    # it won't accept any of the values I've tried for monitoring ref
    assert test_client.stop_timetable("SF", "14148")


@pytest.mark.vcr()
def test_holidays(test_client):
    assert test_client.holidays("SF")
